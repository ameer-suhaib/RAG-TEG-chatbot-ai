from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.services.chat.chat_service import ChatService
from app.services.chat.models import ChatRequest
from app.services.crawler.crawler_service import CrawlerService
from app.services.ingestion.ingestion_service import IngestionService

router = APIRouter()
chat_service = ChatService()


@router.post("/start")
async def start_ingestion():
    """Crawl source pages and return how many were collected."""
    crawler_service = CrawlerService()
    pages = await crawler_service.crawl()
    return {"status": "success", "pages": len(pages)}


@router.post("/ingest")
async def ingest():
    """Process crawled pages: detect language, chunk, embed, store in Qdrant."""
    return await IngestionService().run()


@router.post("/chat")
async def chat(request: ChatRequest):
    """Stream a RAG answer as plain text tokens (UTF-8)."""
    return StreamingResponse(
        chat_service.stream_chat(request),
        media_type="text/plain; charset=utf-8",
    )
