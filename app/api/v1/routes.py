from fastapi import APIRouter
from app.services.crawler.crawler_service import CrawlerService
from app.services.ingestion.ingestion_service import IngestionService
from app.services.processing import ProcessingService

router = APIRouter()


#crawling
@router.post('/start')
async def start_ingestion():
    print("---start_ingestion")
    crawler_service = CrawlerService()
    pages =await crawler_service.crawl()
    return {
        "status": "success",
        "pages": len(pages)
    }

#crawling processing language detect, chunking, embedding, saving(qdrant)
@router.post("/ingest")
async def ingest():
    service = IngestionService()
    return await service.run()