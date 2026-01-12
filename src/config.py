import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Backend Template")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
