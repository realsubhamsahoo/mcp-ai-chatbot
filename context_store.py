import redis
import json
#redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
redis_client = redis.StrictRedis(
    host="your-redis-host",
    port=your-redis-port,
    password="your-redis-password",
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
