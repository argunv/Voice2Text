import aioredis
from config.settings import settings

redis_client = None

async def get_redis_client():
    global redis_client
    if not redis_client:
        redis_client = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            decode_responses=True)
    return redis_client

async def set_key(key: str, value: str, ttl: int = None):
    client = await get_redis_client()
    await client.set(key, value, ex=ttl)

async def get_key(key: str):
    client = await get_redis_client()
    return await client.get(key)
