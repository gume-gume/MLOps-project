from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # DB_NAME="income_db"
    # DB_TABLE="people_incomes"
    # DB_ID="postgres"
    # DB_PASSWORD="postgres"
    # DB_ADDRESS="localhost"
    # REDIS_ADDRESS="localhost"
    # REDIS_PORT=6479
    # REDIS_health_check_interval=30
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings.Config()

settings= get_settings()
