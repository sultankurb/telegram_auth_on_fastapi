from fastapi import HTTPException
from redis.asyncio import Redis

from src.domain.identity.entities import ProfileReadEntity
from src.domain.identity.uow import ProfileUnitOfWork


class GerCurrentUserUseCase:
    def __init__(self, uow: ProfileUnitOfWork, redis: Redis):
        self._uow = uow
        self._redis = redis

    async def execute(self, user_id: int) -> ProfileReadEntity:
        check = await self._redis.get(f"user:{user_id}")
        if check is None:
            async with self._uow as uow:
                user = await uow.profile.find_by_id(id=user_id)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            profile_schema = ProfileReadEntity.model_validate(user)

            await self._redis.setex(
                f"user:{user_id}", 3600, profile_schema.model_dump_json()
            )
            return profile_schema
        return ProfileReadEntity.model_validate_json(check)
