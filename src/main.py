from fastapi import FastAPI
from src.logger import setup_logger

logger = setup_logger()

app = FastAPI(title="FastAPI Backend Template")

@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}
