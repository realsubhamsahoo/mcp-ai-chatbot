import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()  

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True
)

def store_session(user_id, message):
    history = redis_client.get(user_id)
    history = json.loads(history) if history else []
    history.append(message)
    redis_client.set(user_id, json.dumps(history))

def get_recent_messages(user_id, limit=5):
    history = redis_client.get(user_id)
    return json.loads(history)[-limit:] if history else []
