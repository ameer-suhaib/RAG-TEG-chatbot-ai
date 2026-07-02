from datetime import datetime
import logging

from crawl4ai import AsyncWebCrawler

from .models import CrawledPage
from .storage import CrawlStorage
from .url_discovery import URLDiscovery


logger = logging.getLogger(__name__)



class CrawlerService:
    def __init__(self):
        self.discovery = URLDiscovery()
        self.storage = CrawlStorage()

    async def crawl(self) -> list[CrawledPage]:
        urls = await self.discovery.discover()

        logger.info(f"Discovered URL {urls}")

        pages = []

        async with AsyncWebCrawler() as crawler:
            for url in urls:
                logger.info(f"Crawling url {url}")

                try:
                    result =await crawler.arun(url)

                    #build response
                    page = CrawledPage(
                        url = url,
                        title = result.metadata.get("title") if result.metadata else None,
                        markdown=result.markdown if result.markdown else None,
                        html = result.html if result.html else None,
                        status_code=200,
                        success=True,
                        crawled_at=datetime.utcnow()
                    )
                    self.storage.save(page)
                    pages.append(page)
                except Exception as e:
                    logger.exception("Failed crawling %s", url)
                    raise
        logger.info("Successfully crawled %s pages", len(pages))

        return pages