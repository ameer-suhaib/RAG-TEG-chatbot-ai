import logging
from app.services.crawler.models import CrawledPage

from .cleaner import ContentCleaner
from .chunker import DocumentChunker
from .language_detector  import LanguageDetector
from .models import ProcessedChunkDocument
from .processing_manager import get_chunker, get_cleaner, get_language_detector

logger = logging.getLogger(__name__)


class ProcessingService:
    def __init__(self):
        self.cleaner = get_cleaner()
        self.language_detector = get_language_detector()
        self.chunker = get_chunker()


    # process single page
    def process_page(self, page: CrawledPage) -> ProcessedChunkDocument:
        logger.info("Processing %s", page.url)
        logger.info("Raw markdown:\n%s", page.markdown[:3000])

        cleaned = self.cleaner.clean(page.markdown or "")

        language = self.language_detector.detect(cleaned)
        print(language,"-----------language")

        document = self.chunker.chunk(
            page = page,
            cleaned_text=cleaned,
            language=language
        )
        logger.info(
            "Created %d chunks",
            document.total_chunk,
        )

        return document


    #process many pages
    def process_pages(self, pages : list[CrawledPage]) -> ProcessedChunkDocument:
        logger.info("Processing many pages method..")
        documents = []

        for page in pages:
            documents.append(
                self.process_page(page)
            )
        logger.info(
            "processed %d", len(documents)
        )

        return documents