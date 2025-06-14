# utils/gemini_api.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env (MUST be in project root)
load_dotenv()

# Get Gemini API key from environment variable
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_GEMINI_API_KEY not found in environment. Please check your .env file.")

# Configure Gemini API client
genai.configure(api_key=api_key)

def identify_plant(image_bytes):
    """
    Identifies the plant species from image bytes and returns a string with the
    plant name and two interesting facts.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "Identify the plant species in the image and provide 2 short, interesting facts. "
        "Format: First line is the plant name. Next two lines are facts."
    )
    try:
        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": image_bytes},
            prompt
        ])
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {e}"

def plant_care_tips(plant_name):
    """
    Provides concise care instructions for a given plant name.
    """
    prompt = (
        f"Give concise care instructions for {plant_name}:\n"
        "- Watering\n"
        "- Soil type\n"
        "- Sunlight needed\n"
        "Use short bullet points."
    )
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {e}"
