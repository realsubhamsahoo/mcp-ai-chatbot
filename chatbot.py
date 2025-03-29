from openai import OpenAI
from context_store import store_session, get_recent_messages
from vector_store import store_in_vector_db, get_relevant_context
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(api_key=openai_api_key)

def chatbot_response(user_input, user_id):
    recent_messages = get_recent_messages(user_id)
    long_term_context = get_relevant_context(user_input)
    context = "\n".join(recent_messages + [msg.page_content for msg in long_term_context])
    
    response = llm.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI assistant."},
                  {"role": "user", "content": f"Context: {context}\nUser: {user_input}"}]
    ).choices[0].message.content
    
    store_session(user_id, f"User: {user_input}\nBot: {response}")
    store_in_vector_db(user_id, user_input)
    
    return response
