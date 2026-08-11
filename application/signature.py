import hashlib
import hmac
import json
import time

from src.config.config import settings


def generate_telegram_auth_payload(
    bot_token: str = settings.API_TOKEN,
    telegram_id: int = 123456789,
    first_name: str = "Ivan",
    username: str | None = "ivan_dev",
    photo_url: str | None = "https://t.me/i/userpic/320/ivan.jpg",
    auth_date: int | None = None
):
    if auth_date is None:
        auth_date = int(time.time())
    

    payload = {
        "id": telegram_id,
        "first_name": first_name,
        "auth_date": auth_date,
    }
    if username is not None:
        payload.update({"username": username})
    if photo_url is not None:
        payload.update({"photo_url": photo_url})
    payload = {k: v for k, v in payload.items() if v is not None}

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(payload.items())
    )

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    payload["hash"] = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    return json.dumps(payload)

telegram_id = int(input("Enter your Telegram ID: "))
first_name = input("Enter your first name: ")
username = input("Enter your username (optional): ")
photo_url = input("Enter your photo URL (optional): ")

print(generate_telegram_auth_payload(
    telegram_id=telegram_id,
    first_name=first_name,
    username=username,
    photo_url=photo_url,
))