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

    UPLOAD_DIR: str = "uploads"
    UPLOAD_WALLPAPER_DIR: str = "uploads_wallpapers"
    
    PROMPTPAY_ID: str = "0626265127"
    PROMPTPAY_MERCHANT_NAME: str = "Muteverse"
    PROMPTPAY_MERCHANT_CITY: str = "Bangkok"

    class Config:
        env_file = ".env"


settings = Settings()
