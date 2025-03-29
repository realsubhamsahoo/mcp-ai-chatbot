import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
genai.configure(api_key=GENAI_API_KEY)

def chatbot_response(message: str, user_id: str):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(message)
        return response.text  # Get text response
    except Exception as e:
        return f"Error: {str(e)}"
