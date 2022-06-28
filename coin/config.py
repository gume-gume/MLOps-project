import sys
from pydantic import BaseSettings
from functools import lru_cache

sys.path.append("/home/dahy949/airflow/project")


class Settings(BaseSettings):
    DB_NAME: str = "upbit"
    DB_ID: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_ADDRESS: str = "172.26.0.7"
    interval: str = "minute240"
    token: str
    tracking_uri: str = "http://172.26.0.9:5000"
    class Config:
        env_file = "coin/.env"
        print(env_file)


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
