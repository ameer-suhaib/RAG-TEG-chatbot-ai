from contextlib import asynccontextmanager

from fastapi import FastAPI
import asyncio
import logging

from app.api.v1.routes import router as crawlrouter
from app.core.logger import setup_logging
from app.services.embeddings.embedding_manger import get_embedding_model
from app.services.processing.language_detector import LanguageDetector
from app.services.vector_store.qdrant_manager import get_qdrant_client

setup_logging()

logger = logging.getLogger(__name__)


def _warmup_models() -> None:
    logger.info("Warming up embedding model, language detector, and Qdrant client...")
    get_embedding_model()
    LanguageDetector().detect("hello")
    get_qdrant_client()
    logger.info("Model warmup complete.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(_warmup_models)
    yield


app = FastAPI(title="TEG-RAG Bakend", version="1.0.0", lifespan=lifespan)

app.include_router(
    crawlrouter,
    prefix="/app/v1"
)


@app.get('/health')
def health_test():
    logger.info("Health check api calling...")
    return {"message": "hello world!!"}
