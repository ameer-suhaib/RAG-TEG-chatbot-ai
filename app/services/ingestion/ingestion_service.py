from app.services.crawler.crawler_service import CrawlerService
from app.services.processing.processor import ProcessingService
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.vector_store.qdrant_service import QdrantService

from .models import IngestionResult
import logging

logger = logging.getLogger(__name__)

class IngestionService:
    def __init__(self):
        self.crawler = CrawlerService()
        self.processor = ProcessingService()
        self.embedding = EmbeddingService()
        self.qdrant = QdrantService()


    async def run(self) -> IngestionResult:
        """
        Execute the complete flow
        1.crawl website
        2.process page
        3.generate embeddings
        4.store vectos in qdrant
        5.return ingestion summary
        """

        logger.info("===== starting ingestion pipeline======")

        ## step 1 : crawl website
        pages = await self.crawler.crawl(force_refresh=False)
        logger.info("Crawled %d pages", len(pages))

        ## step 2: Process pages
        documents = self.processor.process_pages(pages)
        logger.info("Processed %d documents", len(documents))

        ## step 3 - Flatten all chunks
        chunks = []
        for document in documents:
            chunks.extend(document.chunks)

        logger.info("generated %d chunks", len(chunks))

        if not chunks:
            logger.warning("no chunks generated")

            return IngestionResult(
                pages_crawled=len(pages),
                pages_processed=len(documents),
                chunks_created=0,
                vectors_indexed=0,
                failed_pages=max(0, len(pages) - len(documents)),
            )
        ## step 4 - Generate embeddings
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedding.embed_documents(texts)

        logger.info("Generated %d embeddings", len(embeddings))

        ## step 5 - store in qdrant
        self.qdrant.create_collection()

        self.qdrant.upsert_chunks(
            chunks = chunks,
            embeddings=embeddings,
        )
        logger.info("Indexed %d vectors", len(embeddings))
        logger.info("========== Ingestion completed successfully ==========")
        return IngestionResult(
            pages_crawled=len(pages),
            pages_processed=len(documents),
            chunks_created=len(chunks),
            vectors_indexed=len(embeddings),
            failed_pages=max(0, len(pages) - len(documents)),
        )