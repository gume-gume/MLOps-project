from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DB_NAME = "income_db"
    DB_TABLE = "people_incomes"
    DB_ID = "postgres"
    DB_PASSWORD = "postgres"
    DB_ADDRESS = "172.26.0.7"
    REDIS_ADDRESS = "172.26.0.10"
    REDIS_PORT = 6379
    REDIS_health_check_interval = 30

    class Config:
        env_file = "app/.env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
