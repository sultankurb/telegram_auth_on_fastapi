from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.identity.uow import ProfileUnitOfWork
from src.domain.identity.use_cases.get_user import GerCurrentUserUseCase
from src.domain.identity.use_cases.login import LoginUseCase
from src.infrastructure.auth.jwt_token_service import JWTService
from src.infrastructure.database.connection import session_factory
from src.infrastructure.redis_connection import redis_client

security = HTTPBearer()

async def login_di():
    uow = ProfileUnitOfWork(session=session_factory)
    jwt = JWTService()
    return LoginUseCase(uow, jwt, redis=redis_client)

LoginDepends = Annotated[LoginUseCase, Depends(login_di)]

async def get_payload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:
    token = credentials.credentials
    try:
        jwt_service = JWTService()
        payload = jwt_service.decode_token(token=token)
        return payload

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

async def get_user_di():
    uow = ProfileUnitOfWork(session=session_factory)
    return GerCurrentUserUseCase(uow=uow, redis=redis_client)

GetCurrentUserDepends = Annotated[GerCurrentUserUseCase, Depends(get_user_di)]
PayloadDepends = Annotated[dict, Depends(get_payload)]
