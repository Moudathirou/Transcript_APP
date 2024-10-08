from flask import Flask, render_template, request, jsonify, url_for
import os
from werkzeug.utils import secure_filename

import openai
from groq import Groq
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv

load_dotenv()

# Initialiser l'application Flask
app = Flask(__name__)

# Configurer la clé secrète et le dossier de téléchargement
app.config['SECRET_KEY'] = 'votre_clé_secrète'  # Remplacez par votre clé secrète
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialiser le client OpenAI
openai.api_key = os.getenv('API_KEY') 

api_key_groq = os.getenv('GROQ_API')

# Initialiser le client Groq
groq_client =Groq(api_key=api_key_groq) 

# Extensions de fichiers autorisées
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    print(f"Fichier enregistré à {filepath}")
    return filepath

def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    print(f"Audio extrait vers {audio_path}")
    return audio_path

def transcribe_audio(filename):
    with open(filename, "rb") as file:
        transcription = groq_client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3",
            prompt="Specify context or spelling",
            response_format="verbose_json",
            temperature=0.0
        )

    segments = []
    for segment in transcription.segments:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        segments.append(f"{start_time:.2f} : {end_time:.2f}, {text}")
    
    return segments


def summarize_text_to_bullet_points(text):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Vous êtes un assistant d'interface utilisateur. Votre travail consiste à aider les utilisateurs à visualiser le résumé de leurs textes en les affichant dans un site web."},
            {"role": "user", "content": f"Résumez le texte suivant en un article de blog avec des points clés :\n\n{text}"}
        ]
    )
    summary = response.choices[0].message.content.strip()
    return summary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcription', methods=['POST'])
def transcription():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400
    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = save_file(file, filename)
        # Si le fichier est une vidéo, extraire l'audio
        if filename.lower().endswith(('.mp4', '.avi', '.mov')):
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'audio_from_video.mp3')
            file_path = extract_audio_from_video(file_path, audio_path)
        try:
            transcription_segments = transcribe_audio(file_path)
            transcription_text = '\n'.join(transcription_segments)
            return jsonify({'transcription': transcription_text})
        except Exception as e:
            print(f"Erreur lors de la transcription : {e}")
            return jsonify({'error': 'Une erreur est survenue lors de la transcription.'}), 500
    else:
        return jsonify({'error': 'Type de fichier non autorisé.'}), 400

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    transcription_text = data.get('transcription_text', '')
    if not transcription_text:
        return jsonify({'error': 'Aucun texte de transcription fourni.'}), 400
    try:
        summary = summarize_text_to_bullet_points(transcription_text)
        return jsonify({'summary': summary})
    except Exception as e:
        print(f"Erreur lors du résumé : {e}")
        return jsonify({'error': 'Une erreur est survenue lors du résumé.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
