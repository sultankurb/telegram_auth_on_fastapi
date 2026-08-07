from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class AppConfig(BaseSettings):
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///db.sqlite3"
    REDIS_URL: str = "redis://redis:6379/0"
    API_TOKEN: str = ""
    title: str = "My API"
    description: str = "My description"
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


def get_app_config() -> AppConfig:
    return AppConfig()


settings = get_app_config()
