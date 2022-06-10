from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DB_NAME = "upbit"
    DB_ID = "postgres"
    DB_PASSWORD = "postgres"
    DB_ADDRESS = "0.0.0.0"
    ticker = "KRW-BTC"
    interval = "minutes240"
    token = ""

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
