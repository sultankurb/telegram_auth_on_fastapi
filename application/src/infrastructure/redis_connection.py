from redis.asyncio import from_url

from src.config.config import settings

redis_client = from_url(
    url=settings.REDIS_URL,
    max_connections=20,
    socket_timeout=5.0,
    decode_responses=True,
)