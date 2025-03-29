import pinecone
import os
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

load_dotenv()  # Load env variables

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV", "us-west1-gcp")
)
index_name = "chatbot-memory"

if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536)

embeddings = OpenAIEmbeddings()
vector_store = Pinecone.from_existing_index(index_name, embeddings)

def store_in_vector_db(user_id, message):
    vector_store.add_texts([message], metadatas=[{"user_id": user_id}])

def get_relevant_context(user_input):
    return vector_store.similarity_search(user_input, k=3)
