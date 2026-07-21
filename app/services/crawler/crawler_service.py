from datetime import datetime, timezone
import json
import logging

from crawl4ai import AsyncWebCrawler
from urllib.parse import urljoin

from app.services.pdf_urls.pdf_service import PdfService

from .crawl_mananger import (
    get_browser_config,
    get_crawler_run_config,
)
from .models import CrawledPage
from .storage import CrawlStorage
from .url_discovery import URLDiscovery

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_HTML_DIR = BASE_DIR / "storage" / "raw_html"

def has_existing_data() -> bool:
    return RAW_HTML_DIR.exists() and any(RAW_HTML_DIR.iterdir())

logger = logging.getLogger(__name__)


class CrawlerService:
    def __init__(self):
        self.discovery = URLDiscovery()
        self.storage = CrawlStorage()
        self.pdf_service = PdfService()
        self.browser_config = get_browser_config()
        self.run_config = get_crawler_run_config()

    async def crawl(self, force_refresh: bool = True) -> list[CrawledPage]:


        print(force_refresh,has_existing_data())
        if not force_refresh and has_existing_data():
            logger.info("Raw crawl data already exists. Skipping crawl.")
            return self.storage.load_all()
        urls = await self.discovery.discover()
        

        logger.info("Discovered %d URLs", len(urls))

        pages: list[CrawledPage] = []
        failed_pages = 0
        all_pdf_urls: set[str] = set()

        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            for index, url in enumerate(urls, start=1):

                logger.info("[%d/%d] Crawling %s", index, len(urls), url)

                try:
                    result = await crawler.arun(
                        url=url,
                        config=self.run_config,
                    )
                    
                    if not result.success:
                        logger.warning(
                            "Failed crawling %s: %s",
                            url,
                            result.error_message,
                        )
                        failed_pages += 1
                        continue
                    # Collect PDF URLs from this page
                    if result.links:
                        for link in result.links.get("internal", []):
                            href = link.get("href")

                            if not href:
                                continue

                            absolute = urljoin(url, href)

                            if absolute.lower().endswith(".pdf"):
                                all_pdf_urls.add(absolute)
                    print("pdf_urlss---", all_pdf_urls)
                    print("RAW MARKDOWN")
                    print(result.markdown.raw_markdown[:2000])
                    logger.info("Discovered %d unique PDF URLs", len(all_pdf_urls))

                    page = CrawledPage(
                        url=url,
                        title=result.metadata.get("title") if result.metadata else None,
                        markdown=result.markdown.raw_markdown if result.markdown else None,
                        html=result.html,
                        status_code=result.status_code,
                        success=result.success,
                        crawled_at=datetime.now(timezone.utc),
                    )

                    self.storage.save(page)
                    pages.append(page)


                except Exception:
                    logger.exception("Failed crawling %s", url)
                    failed_pages += 1
            

        logger.info(
            "Crawl completed. Success=%d Failed=%d",
            len(pages),
            failed_pages,
        )

        logger.info("Found %d unique PDF files", len(all_pdf_urls))

        for index, pdf_url in enumerate(sorted(all_pdf_urls), start=1):
            logger.info(
                "[PDF %d/%d] Processing %s",
                index,
                len(all_pdf_urls),
                pdf_url,
            )

            try:
                pdf_page = await self.pdf_service.load(pdf_url)

                self.storage.save(pdf_page)
                pages.append(pdf_page)

            except Exception:
                logger.exception("Failed processing PDF: %s", pdf_url)
                failed_pages += 1
        return pages