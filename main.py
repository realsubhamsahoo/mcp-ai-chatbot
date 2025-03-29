from fastapi import FastAPI
from chatbot import chatbot_response

app = FastAPI()

@app.post("/chat/")
async def chat(user_id: str, message: str):
    response = chatbot_response(message, user_id)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
