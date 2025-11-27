# Uncomment these lines at the top
from dotenv import load_dotenv
load_dotenv()

# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1: Setup Gemini API key
import os

GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY")

#Step2: Convert image to required format
import base64
from PIL import Image

def encode_image(image_path):   
    """Load image for Gemini API - returns PIL Image object"""
    try:
        # Open and load image, ensuring it's fully loaded into memory
        image = Image.open(image_path)
        # Load the image data into memory (important for closed file handles)
        image.load()
        # Convert to RGB if necessary (for PNG with transparency, etc.)
        if image.mode != "RGB":
            image = image.convert("RGB")
        # Create a copy to ensure the image is independent of the file
        return image.copy()
    except Exception as e:
        raise Exception(f"Error loading image: {str(e)}")

#Step3: Setup Multimodal LLM with Google Gemini
import google.generativeai as genai

def analyze_image_with_query(query, model, encoded_image):
    """
    Analyze image using Google Gemini API
    
    Args:
        query: Text query/prompt
        model: Model name (e.g., "gemini-1.5-pro" or "gemini-1.5-flash")
        encoded_image: PIL Image object
    """
    # Get API key from environment
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Use the model (default to gemini-2.0-flash for faster responses)
        model_name = model if model else "gemini-2.0-flash"
        gemini_model = genai.GenerativeModel(model_name)
        
        # Generate response with image and text
        response = gemini_model.generate_content([query, encoded_image])
        
        # Extract text from response
        if response.text:
            return response.text
        else:
            raise Exception("No response text from Gemini API")
            
    except Exception as e:
        error_msg = f"Gemini API error: {str(e)}"
        raise Exception(error_msg)