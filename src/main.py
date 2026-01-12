from fastapi import FastAPI
from src.config import settings
from src.routes.health import router as health_router

app = FastAPI(title=settings.APP_NAME)

app.include_router(health_router)
