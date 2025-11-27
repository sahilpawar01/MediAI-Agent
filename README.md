# AI Doctor with Vision and Voice

A medical AI assistant that analyzes images and processes voice input to provide medical insights using:
- **Groq API** for speech-to-text transcription
- **Google Gemini API** for image analysis
- **gTTS** for text-to-speech responses

## Features

- 🎤 Voice input transcription
- 🖼️ Medical image analysis
- 💬 AI-powered medical responses
- 🔊 Audio response generation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

3. Run the app:
```bash
python gradio_app.py
```

## Deployment

### Option 1: Hugging Face Spaces (Recommended)

1. Create a new Space at https://huggingface.co/spaces
2. Select "Gradio" as the SDK
3. Push your code to the repository
4. Add secrets (API keys) in Settings → Secrets:
   - `GROQ_API_KEY`
   - `GEMINI_API_KEY`

### Option 2: Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python app.py`
5. Add environment variables:
   - `GROQ_API_KEY`
   - `GEMINI_API_KEY`

## Requirements

- Python 3.10+
- See `requirements.txt` for full list of dependencies

