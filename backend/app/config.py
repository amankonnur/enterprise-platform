from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    JWT_SECRET_KEY: str

    class Config:
        # Use absolute path to ensure it loads correctly
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        env_file_encoding = 'utf-8'

settings = Settings()
