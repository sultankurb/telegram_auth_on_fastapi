import hashlib
import hmac
import time

import requests
from src.config.config import settings

import json


def generate_telegram_auth_payload(
    bot_token: str = settings.API_TOKEN,
    user_id: int = 123456789,
    first_name: str = "Ivan",
    username: str | None = "ivan_dev",
    photo_url: str | None = "https://t.me/i/userpic/320/ivan.jpg",
):
    auth_date = int(time.time())

    payload = {
        "telegram_id": user_id,
        "first_name": first_name,
        "username": username,
        "photo_url": photo_url,
        "auth_date": auth_date,
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(payload.items())
    )

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    payload["hash"] = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    return payload
request = requests.post(
    url="http://0.0.0.0:8000/api/auth/telegram",
    json=generate_telegram_auth_payload()
)

print(generate_telegram_auth_payload())
print(request.status_code)
print(request.json())