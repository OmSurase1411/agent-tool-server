from fastapi import APIRouter
from src.logger import setup_logger
from src.config import settings

router = APIRouter()
logger = setup_logger()

@router.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {
        "status": "ok",
        "app": settings.APP_NAME
    }
