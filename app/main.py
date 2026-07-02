from fastapi import FastAPI
import logging
from .api.v1.routes import router as crawlrouter

from app.core.logger import setup_logging


setup_logging()

logger = logging.getLogger(__name__)


app = FastAPI(title="TEG-RAG Bakend", version="1.0.0")

app.include_router(
    crawlrouter,
    prefix="/app/v1"
)


@app.get('/health')
def health_test():
    logger.info("Health check api calling...")
    return {"message":"hello world!!"}