import hashlib
import hmac
import time
from typing import Any

from src.config.config import settings


def verify_telegram_data(
    data: dict[str, Any],
    bot_token: str = settings.API_TOKEN,
    max_age_seconds: int = 86400,
) -> bool:
    data_copy = {k: v for k, v in data.items() if v is not None}
    received_hash = data_copy.pop("hash", None)
    auth_date = data_copy.get("auth_date")

    if not received_hash or auth_date is None:
        return False

    try:
        if time.time() - int(auth_date) > max_age_seconds:
            return False
    except (ValueError, TypeError):
        return False

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(data_copy.items())
    )

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(calculated_hash, str(received_hash))
