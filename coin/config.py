from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DB_NAME = "upbit"
    DB_ID = "postgres"
    DB_PASSWORD = "postgres"
    DB_ADDRESS = "localhost"
    ticker = "KRW-LTC"
    interval = "minutes240"

    class Config:
        env_file = "coin/.env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
