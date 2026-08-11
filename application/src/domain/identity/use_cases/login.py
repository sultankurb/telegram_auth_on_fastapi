from typing import Any

from redis.asyncio import Redis

from src.domain.identity.interfaces.jwt_interface import JWTInterface
from src.domain.identity.uow import ProfileUnitOfWork


class LoginUseCase:
    def __init__(
        self, uow: ProfileUnitOfWork, jwt: JWTInterface, redis: Redis
    ) -> None:
        self._uow = uow
        self._jwt = jwt
        self._redis = redis

    async def execute(self, schema: dict) -> dict[str, Any]:
        async with self._uow as uow:
            result = await uow.profile.upsert_telegram_user(user_data=schema)
            await uow.commit()
        tokens = await self._jwt.create_user_session(
            user_id=result.id, redis=self._redis
        )
        return tokens
