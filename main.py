import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Please set it in your .env file.")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize FastAPI app
app = FastAPI()

# Request model
class ChatRequest(BaseModel):
    user_id: str
    message: str

# Chatbot function
def chatbot_response(message: str, user_id: str):
    try:
        model_name = "gemini-2.0-flash"  # Change if needed
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(message)
        return response.text if response else "No response from model."
    except Exception as e:
        return f"Error: {str(e)}"

# API Route
@app.post("/chat/")
async def chat(request: ChatRequest):
    response = chatbot_response(request.message, request.user_id)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
