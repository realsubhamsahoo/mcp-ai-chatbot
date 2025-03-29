import os
from dotenv import load_dotenv
import pinecone
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone as LangchainPinecone

# Load environment variables
load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp")
index_name = os.getenv("PINECONE_INDEX_NAME", "mcp-ai-chatbot")

if not api_key:
    raise ValueError("Missing Pinecone API Key! Please set it in the .env file.")

# Initialize Pinecone
pinecone.init(api_key=api_key, environment=environment)

# Create index if it does not exist
if index_name not in pinecone.list_indexes():
    print(f"Creating Pinecone index: {index_name}")
    pinecone.create_index(index_name, dimension=1536, metric="cosine")

# Connect to the index
index = pinecone.Index(index_name)

# Initialize Langchain Pinecone vector store
embeddings = OpenAIEmbeddings()
vector_store = LangchainPinecone(index, embeddings)

def store_in_vector_db(text, metadata=None):
    """
    Store text in the Pinecone vector database.
    """
    vector_store.add_texts(texts=[text], metadatas=[metadata or {}])
    print(f"Stored text: {text[:50]}...")

def get_relevant_context(query, top_k=5):
    """
    Retrieve relevant context from the vector store based on a query.
    """
    results = vector_store.similarity_search(query, k=top_k)
    return [result.page_content for result in results]
