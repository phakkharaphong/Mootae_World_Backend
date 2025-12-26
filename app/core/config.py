from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_MODE: str = "local"

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    ACCESS_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str
    HASHING_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    UPLOAD_DIR: str = str(Path(__file__).resolve().parents[2] / "uploads")

    class Config:
        env_file = ".env"


settings = Settings()
