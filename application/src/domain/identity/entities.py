from datetime import datetime

from pydantic import BaseModel, Field


class BaseProfileEntity(BaseModel):
    telegram_id: int = Field(..., description='Telegram user id', gt=0)
    username: str | None = Field(..., description="Username", min_length=1)
    first_name: str = Field(..., description="First name", min_length=1)
    photo_url: str | None = Field(..., description="Photo url")

    class Config:
        from_attributes = True


class ProfileReadEntity(BaseProfileEntity):
    id: int = Field(..., description='User id', gt=0)
    created_at: datetime = Field(..., description='time when user created')


class TelegramLoginEntity(BaseModel):
    telegram_id: int = Field(..., description='Telegram user id', gt=0)
    username: str | None = Field(..., description='Username', min_length=1)
    first_name: str = Field(..., description='First name', min_length=1)
    photo_url: str | None = Field(..., description='Photo url')
    hash: str = Field(
        ...,
        pattern=r"^[a-fA-F0-9]{64}$",
        description="HMAC-SHA256 hash"
    )
    auth_date: int = Field(..., gt=0, description="UNIX timestamp auth")

    class Config:
        from_attributes = True
