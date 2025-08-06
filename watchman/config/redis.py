from watchman.config.model import model_settings
from redis.asyncio import Redis
import json
import hashlib

_redis = Redis(
    host=model_settings.REDIS_HOST,
    port=model_settings.REDIS_PORT,
    db=0,
    decode_responses=True,
    encoding='utf-8'
)

async def cache_query_result(query: str, service: str, result: dict, ttl: int = 300):
    key = f"log_query:{hashlib.md5(f'{query}:{service}'.encode()).hexdigest()}"
    await _redis.set(key, json.dumps(result), ex=ttl)

async def get_cached_query_result(query: str, service: str) -> dict:
    key = f"log_query:{hashlib.md5(f'{query}:{service}'.encode()).hexdigest()}"
    cached = await _redis.get(key)
    return json.loads(cached) if cached else None

async def cache_embeddings(log_id: str, embedding: list, ttl: int = 3600):
    key = f"embedding:{log_id}"
    await _redis.set(key, json.dumps(embedding), ex=ttl)

async def get_cached_embeddings(log_id: str) -> list:
    key = f"embedding:{log_id}"
    cached = await _redis.get(key)
    return json.loads(cached) if cached else None