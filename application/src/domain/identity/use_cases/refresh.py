from redis.asyncio import Redis

from src.config.exeptions import ForbiddenException
from src.domain.identity.entities import TokenEntity
from src.domain.identity.interfaces.jwt_interface import JWTInterface
from src.domain.identity.uow import ProfileUnitOfWork


class RefreshTokenUseCase:
    def __init__(
        self, jwt_service: JWTInterface, redis: Redis, uow: ProfileUnitOfWork
    ):
        self._jwt_service = jwt_service
        self._redis = redis
        self._uow = uow

    async def execute(self, refresh_token: str) -> TokenEntity:
        query = f"refresh_token:{refresh_token}"
        user_id = await self._redis.get(query)
        if user_id is None:
            raise ForbiddenException(
                message="There is no user with this refresh token"
            )
        async with self._uow as uow:
            profile = await uow.profile.find_by_id(id=int(user_id))
            if profile is None:
                raise ForbiddenException(
                    message="User associated with this token no longer exists"
                )
            id = profile.id

        new_tokens = await self._jwt_service.create_user_session(
            user_id=id, redis=self._redis
        )
        await self._redis.delete(query)
        return TokenEntity.model_validate(new_tokens)
