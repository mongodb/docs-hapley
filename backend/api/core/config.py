from functools import lru_cache
from os import getenv

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Hapley API"
    description: str = "API for Hapley, the MongoDB docs platform management tool"
    mongo_uri: str = getenv("MONGO_URI")
    mongo_db_name: str = getenv("MONGO_DB_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
