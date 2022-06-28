from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DB_NAME :str = "income_db"
    DB_TABLE :str = "people_incomes"
    DB_ID :str = "postgres"
    DB_PASSWORD :str = "postgres"
    DB_ADDRESS :str = "172.26.0.7"
    REDIS_ADDRESS :str = "172.26.0.10"
    REDIS_PORT :int = 6379
    REDIS_health_check_interval :int = 30

    MINIO_ACCESS_KEY :str = "minioadmin"
    MINIO_SECRET_KEY :str = "minioadmin"
    MINIO_ADDRESS :str = "172.26.0.6"
    MINIO_PORT :int = 9000

    tracking_uri:str = "http://172.26.0.9:5000"
    class Config:
        env_file = "app/.env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
