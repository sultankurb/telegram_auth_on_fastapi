from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.domain.identity.entities import TelegramLoginEntity
from src.infrastructure.auth.hash_validator import verify_telegram_data
from src.presentation.api.dependencies import security
from src.presentation.api.depends_annotaions import (
    GetCurrentUserDepends,
    LoginDepends,
    LogOutDepends,
    PayloadDepends,
    RefreshDepends,
)

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

@router.get(path="/me", status_code=status.HTTP_200_OK)
async def get_my_profile(
        payload: PayloadDepends,
        use_case: GetCurrentUserDepends
):
    user_id = int(payload.get("sub"))
    user = await use_case.execute(user_id=user_id)
    return user

@router.post(path="/auth/telegram", status_code=status.HTTP_201_CREATED)
async def sign_in_by_telegram(
        schema: TelegramLoginEntity,
        login: LoginDepends
):
    payload = schema.model_dump(exclude_none=True)
    verify = verify_telegram_data(data=payload)
    payload.pop("hash")
    payload.pop("auth_date")
    if not verify:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    result = await login.execute(schema=payload)
    return result

@router.post(path="/auth/refresh", status_code=status.HTTP_200_OK)
async def refresh(refresh_token: str, use_case: RefreshDepends):
    result = await use_case.execute(refresh_token=refresh_token)
    return result

@router.post(path="/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
        token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        use_case: LogOutDepends
):
    await use_case.execute(token=token.credentials)
