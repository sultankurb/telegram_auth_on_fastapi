from redis.asyncio import Redis


class LogOutUseCase:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def execute(self, token: str) -> None:
        await self._redis.setex(f"logout:token:{token}", 1200, 1)
