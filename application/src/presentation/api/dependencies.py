from typing import Annotated

from fastapi import Depends

from src.domain.identity.uow import ProfileUnitOfWork
from src.domain.identity.use_cases.login import LoginUseCase
from src.infrastructure.auth.jwt_token_service import JWTService
from src.infrastructure.database.connection import session_factory
from src.infrastructure.redis_connection import redis_client


async def login_di():
    uow = ProfileUnitOfWork(session=session_factory)
    jwt = JWTService()
    return LoginUseCase(uow, jwt, redis=redis_client)

LoginDepends = Annotated[LoginUseCase, Depends(login_di)]