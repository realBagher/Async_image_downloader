from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field

from typing import Optional
import logging


logging.basicConfig(
    level=logging.INFO,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.FileHandler("settings.log"),  # Log to a file
        logging.StreamHandler(),  # Log to the console
    ],
)


class Settings(BaseSettings):
    # Database configurations
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(..., env="POSTGRES_PORT")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    DATABASE_URL: Optional[PostgresDsn] = None

    API_KEY: str = Field(..., env="API_KEY")
    SEARCH_ENGINE_ID: str = Field(..., env="SEARCH_ENGINE_ID")

    DEBUG: bool = Field(False, env="DEBUG")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


def get_settings() -> Settings:
    return settings


# settings.py
if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    print("Loaded Settings:")
    print(settings.dict())
