from datetime import timedelta
from pathlib import Path

from pydantic import BaseModel


class JWTConfig(BaseModel):
    private_key: Path
    public_key: Path
    algorithm: str = "RS256"
    access_token_expire: timedelta = timedelta(minutes=20)
    refresh_token_expire: timedelta = timedelta(days=7)
