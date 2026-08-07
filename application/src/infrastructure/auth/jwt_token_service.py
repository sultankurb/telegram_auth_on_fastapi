import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from redis.asyncio import Redis

from src.config.config import settings
from src.config.exeptions import ApplicationException

PRIVATE_KEY = settings.jwt.private_key.read_text()
PUBLIC_KEY = settings.jwt.public_key.read_text()


class JWTService:
    def __init__(
        self,
        private_key: str = PRIVATE_KEY,
        public_key: str = PUBLIC_KEY,
        algorithm: str = settings.jwt.algorithm,
        access_expire_minutes: timedelta = settings.jwt.access_expire_minutes,
        refresh_expire_days: timedelta = settings.jwt.access_token_expire,
    ) -> None:
        self._private_key = private_key
        self._public_key = public_key
        self._algorithm = algorithm
        self._access_expire = access_expire_minutes
        self._refresh_expire = refresh_expire_days

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            decoded = jwt.decode(
                jwt=token, key=self._public_key, algorithms=[self._algorithm]
            )
            return decoded
        except jwt.PyJWTError:
            raise ApplicationException

    def _encode_token(self, payload: dict[str, Any]) -> str:
        to_encode = payload.copy()
        now = datetime.now(tz=UTC)
        expire = now + self._access_expire
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            payload=to_encode,
            key=self._private_key,
            algorithm=self._algorithm,
        )
        return encoded

    def _create_access_token(self, user_pk: int) -> str:
        jwt_payload = {
            "sub": str(user_pk),
        }
        return self._encode_token(payload=jwt_payload)

    @staticmethod
    def _create_refresh_token():
        return secrets.token_hex(32)

    async def create_user_session(
        self,
        user_id: int,
        redis: Redis,
    ) -> dict:
        access_token = self._create_access_token(user_id)
        refresh_token = self._create_refresh_token()
        refresh_token_expire = int(self._refresh_expire.total_seconds())
        async with redis.pipeline() as pipe:
            await pipe.setex(
                f"refresh_token:{refresh_token}", refresh_token_expire, user_id
            )
            await pipe.sadd(f"user_sessions:{user_id}", refresh_token)
            await pipe.expire(f"user_sessions:{user_id}", refresh_token_expire)
            await pipe.execute()

        return {"access_token": access_token, "refresh_token": refresh_token}
