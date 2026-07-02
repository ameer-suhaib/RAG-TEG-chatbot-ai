from fastapi import APIRouter
from app.services.crawler.crawler_service import CrawlerService

router = APIRouter()

crawler_service = CrawlerService()

@router.post('/start')
async def start_ingestion():
    print("---start_ingestion")
    pages =await crawler_service.crawl()
    return {
        "status": "success",
        "pages": len(pages)
    }