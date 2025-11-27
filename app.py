# This is the main entry point for deployment platforms
# It's the same as gradio_app.py but with deployment-friendly settings

from dotenv import load_dotenv
load_dotenv()

import os
import gradio as gr
import logging
import traceback

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = ""
    doctor_response = ""
    voice_of_doctor = None
    
    try:
        logging.info("Processing new request...")
        
        # Check API keys
        groq_api_key = os.environ.get("GROQ_API_KEY")
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        
        if not groq_api_key:
            error_msg = "Error: GROQ_API_KEY not found in environment variables."
            logging.error(error_msg)
            return error_msg, error_msg, None
        
        if not gemini_api_key:
            error_msg = "Error: GEMINI_API_KEY not found in environment variables."
            logging.error(error_msg)
            return error_msg, error_msg, None
        
        # Handle audio input
        if audio_filepath is not None:
            if isinstance(audio_filepath, tuple):
                audio_filepath = audio_filepath[0]
            
            if not os.path.exists(audio_filepath):
                speech_to_text_output = f"Audio file not found: {audio_filepath}"
            else:
                try:
                    speech_to_text_output = transcribe_with_groq(
                        stt_model="whisper-large-v3",
                        audio_filepath=audio_filepath,
                        GROQ_API_KEY=groq_api_key
                    )
                except Exception as e:
                    speech_to_text_output = f"Error transcribing audio: {str(e)}"
        else:
            speech_to_text_output = "No audio provided"

        # Handle image input
        if image_filepath is not None:
            if isinstance(image_filepath, dict):
                image_filepath = image_filepath.get("path") or image_filepath.get("name")
            
            if not os.path.exists(image_filepath):
                doctor_response = f"Image file not found: {image_filepath}"
            else:
                try:
                    query = system_prompt + " " + speech_to_text_output if speech_to_text_output != "No audio provided" and not speech_to_text_output.startswith("Error") else system_prompt
                    
                    encoded_img = encode_image(image_filepath)
                    doctor_response = analyze_image_with_query(
                        query=query,
                        model="gemini-2.0-flash",
                        encoded_image=encoded_img
                    )
                except Exception as e:
                    doctor_response = f"Error analyzing image: {str(e)}"
        else:
            doctor_response = "No image provided for me to analyze"

        # Generate audio response
        if doctor_response and not doctor_response.startswith("Error") and doctor_response != "No image provided for me to analyze":
            try:
                audio_output_path = os.path.abspath("final.mp3")
                voice_of_doctor = text_to_speech_with_gtts(input_text=doctor_response, output_filepath=audio_output_path)
                
                if not os.path.exists(voice_of_doctor):
                    voice_of_doctor = None
            except Exception as e:
                logging.error(f"Error generating audio: {e}")
                voice_of_doctor = None

        return str(speech_to_text_output) if speech_to_text_output else "", str(doctor_response) if doctor_response else "", voice_of_doctor
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logging.error(error_msg)
        logging.error(traceback.format_exc())
        return error_msg, error_msg, None


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice Response", type="filepath")
    ],
    title="AI Doctor with Vision and Voice",
    description="Upload an image and audio to get medical analysis from an AI doctor."
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)

