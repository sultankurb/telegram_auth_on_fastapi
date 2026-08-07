from datetime import datetime

from pydantic import BaseModel


class BaseProfileEntity(BaseModel):
    telegram_id: int
    username: str | None = None
    first_name: str
    photo_url: str | None = None


class ProfileReadEntity(BaseProfileEntity):
    id: int
    created_at: datetime
    from datetime import datetime

    from pydantic import BaseModel

    class BaseProfileEntity(BaseModel):
        telegram_id: int
        username: str | None = None
        first_name: str
        photo_url: str | None = None

    class Config:
        from_attributes = True

class TelegramLoginEntity(BaseModel):
    id: int
    username: str | None = None
    first_name: str
    photo_url: str | None = None
    hash: str
    auth_date: datetime

    class Config:
        from_attributes = True
