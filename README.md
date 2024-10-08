

**Audio/Video Transcription & Summary App** est une application intuitive permettant de transcrire des fichiers audio ou vidéo en texte et de résumer automatiquement les transcriptions. Téléchargez un fichier audio ou vidéo, obtenez instantanément la transcription, et générez un résumé en un clic !

## 🚀 Fonctionnalités

- **Transcription automatique** : Téléchargez simplement votre fichier audio ou vidéo, et la transcription s'affichera automatiquement grâce à Whisper optimisé pour Groq.
- **Résumé en un clic** : Une fois la transcription affichée, cliquez sur le bouton **"Résumer"** pour obtenir un résumé concis grâce à OpenAI GPT-4o-mini.
- **Support de multiples formats** : Prend en charge les formats audio et vidéo les plus courants, comme MP3, WAV, MP4, et bien plus encore.
- **Export facile** : Téléchargez les transcriptions et les résumés pour une utilisation ultérieure sous forme de fichiers texte.
- **Interface utilisateur intuitive** : Conçue pour être accessible à tous, même sans compétences techniques avancées.

## 🛠️ Technologies utilisées

- **Whisper sur Groq** : Pour une transcription rapide et précise des fichiers audio et vidéo.
- **OpenAI GPT-4o-mini** : Pour générer des résumés intelligents et concis à partir des transcriptions.
- **Python 3.9** : Langage de programmation pour le backend, garantissant la stabilité et la performance.

## 📥 Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/username/transcription-app.git
   cd transcription-app
   
2. Installez les dépendances :
   ```bash

   pip install -r requirements.txt
   
3. Lancez l'application :
   ```bash
   python main.py

   
## 🔧 Configuration
Clé API OpenAI : Vous aurez besoin d'une clé API OpenAI pour accéder à GPT-4o-mini mais aussi la clé API GROQ pour faire fonctionner whisper. Placez-les dans un fichier .env :

   ```bash

   OPENAI_API_KEY=your_api_key_here
   GROQ_API_KEY=your_api_key_here


