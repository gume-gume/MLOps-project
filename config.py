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
    AWS_BUCKET_NAME: str
    AWS_REGION: str
    MLFLOW_S3_ENDPOINT_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    MLFLOW_URL: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
