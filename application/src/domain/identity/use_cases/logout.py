from redis.asyncio import Redis


class LogOutUseCase:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def execute(self, token: str, user_id: int) -> None:
        await self._redis.setex(f"logout:token:{token}", 1200, 1)
        refresh_tokens = await self._redis.smembers(f"user_sessions:{user_id}")
        async with self._redis.pipeline() as pipe:
            for refresh_token in refresh_tokens:
                pipe.delete(f"refresh_token:{refresh_token}")

            pipe.delete(f"user_sessions:{user_id}")

            await pipe.execute()
