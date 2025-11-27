# Uncomment these lines at the top
from dotenv import load_dotenv
load_dotenv()

# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1: Setup Audio recorder (ffmpeg & portaudio)
# NOTE: record_audio function is not used in deployment - Gradio handles audio recording
# The imports are optional and only needed if you want to use record_audio locally

import logging

# Optional imports for record_audio function (not used in deployment)
# These are only imported if speech_recognition is available
try:
    import speech_recognition as sr
    from pydub import AudioSegment
    from io import BytesIO
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    # speech_recognition not available - this is fine for deployment
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None
    AudioSegment = None
    BytesIO = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.
    NOTE: This function is not used in the deployed app - Gradio handles audio recording.
    Only available if speech_recognition is installed (for local development).
    
    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_lfimit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    if not SPEECH_RECOGNITION_AVAILABLE:
        raise ImportError("speech_recognition is not available. This function is not used in deployment.")
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Commented out - this was running at module import time
# audio_filepath="patient_voice_test_for_patient.mp3"
# record_audio(file_path=audio_filepath)

#Step2: Setup Speech to text–STT–model for transcription
import os
from groq import Groq

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
stt_model="whisper-large-v3"

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client=Groq(api_key=GROQ_API_KEY)
    
    with open(audio_filepath, "rb") as audio_file:
        transcription=client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )

    return transcription.text