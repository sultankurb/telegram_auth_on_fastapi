from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.identity.uow import ProfileUnitOfWork
from src.domain.identity.use_cases.get_user import GerCurrentUserUseCase
from src.domain.identity.use_cases.login import LoginUseCase
from src.domain.identity.use_cases.logout import LogOutUseCase
from src.domain.identity.use_cases.refresh import RefreshTokenUseCase
from src.infrastructure.auth.jwt_token_service import JWTService
from src.infrastructure.database.connection import session_factory
from src.infrastructure.redis_connection import redis_client

security = HTTPBearer()


async def login_di() -> LoginUseCase:
    uow = ProfileUnitOfWork(session=session_factory)
    jwt = JWTService()
    return LoginUseCase(uow, jwt, redis=redis_client)


async def get_payload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    token = credentials.credentials
    check = await redis_client.get(f"logout:token:{token}")
    if check is not None:
        raise exception
    try:
        jwt_service = JWTService()
        payload = jwt_service.decode_token(token=token)
        return payload

    except Exception:
        raise exception


async def get_user_di() -> GerCurrentUserUseCase:
    uow = ProfileUnitOfWork(session=session_factory)
    return GerCurrentUserUseCase(uow=uow, redis=redis_client)


async def refresh_di() -> RefreshTokenUseCase:
    jwt_service = JWTService()
    uow = ProfileUnitOfWork(session=session_factory)
    return RefreshTokenUseCase(
        uow=uow, jwt_service=jwt_service, redis=redis_client
    )


async def logout_di() -> LogOutUseCase:
    return LogOutUseCase(redis=redis_client)
