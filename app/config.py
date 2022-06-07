from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DB_NAME: str
    DB_TABLE: str
    DB_ID: str
    DB_PASSWORD: str
    DB_ADDRESS: str
    REDIS_ADDRESS: str
    REDIS_PORT: int
    REDIS_health_check_interval: int

    class Config:
        env_file = "app/.env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
