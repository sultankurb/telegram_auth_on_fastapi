from fastapi import APIRouter, HTTPException, status

from src.domain.identity.entities import TelegramLoginEntity
from src.infrastructure.auth.hash_validator import verify_telegram_data
from src.presentation.api.dependencies import (
    GetCurrentUserDepends,
    LoginDepends,
    PayloadDepends,
)

router = APIRouter(
    prefix="/api",
)

@router.get(path="/me")
async def get_my_profile(
        payload: PayloadDepends,
        use_case: GetCurrentUserDepends
):
    user_id = int(payload.get("sub"))
    user = await use_case.execute(user_id=user_id)
    return user

@router.post(path="/auth/telegram")
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

