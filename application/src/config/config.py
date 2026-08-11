from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.jwt_config import JWTConfig

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PUBLIC_KEY_PATH = BASE_DIR / "certificates" / "public-key.pem"
PRIVATE_KEY_PATH = BASE_DIR / "certificates" / "private-key.pem"


class AppConfig(BaseSettings):
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///db.sqlite3"
    REDIS_URL: str = "redis://redis:6379/0"
    API_TOKEN: str = ""
    title: str = "My API"
    description: str = "My description"
    jwt: JWTConfig = JWTConfig(
        private_key=PRIVATE_KEY_PATH,
        public_key=PUBLIC_KEY_PATH,
    )
    CORS_ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
        "http://127.0.0.1:8000",
    ]
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


def get_app_config() -> AppConfig:
    return AppConfig()


settings = get_app_config()
