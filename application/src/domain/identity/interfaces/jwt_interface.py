from typing import Any, Protocol

from redis.asyncio import Redis


class JWTInterface(Protocol):
    async def create_user_session(
            self,
            user_id: int,
            redis: Redis,
    ) -> dict:
        pass

    def decode_token(self, token: str) -> dict[str, Any]:
        pass
