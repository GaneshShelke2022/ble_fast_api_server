import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "blemeshapp"
    DB_USER: str = "root"
    DB_PASSWORD: str = "keetronics123"

    JWT_SECRET: str = "touchmatik_secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")


settings = Settings()


def get_settings() -> Settings:
    return settings
