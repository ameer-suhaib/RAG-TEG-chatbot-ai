from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.services.chat.chat_service import ChatService
from app.services.chat.models import ChatRequest
from app.services.crawler.crawler_service import CrawlerService
from app.services.ingestion.ingestion_service import IngestionService

router = APIRouter()

chat_service = ChatService()


#crawling
@router.post('/start')
async def start_ingestion():
    print("---start_ingestion")
    crawler_service = CrawlerService()
    pages = await crawler_service.crawl()
    return {
        "status": "success",
        "pages": len(pages)
    }

#crawling processing language detect, chunking, embedding, saving(qdrant)
@router.post("/ingest")
async def ingest():
    service = IngestionService()
    return await service.run()


#chat (streaming)
@router.post('/chat')
async def chat(request: ChatRequest):
    return StreamingResponse(
        chat_service.stream_chat(request),
        media_type="text/plain; charset=utf-8",
    )
