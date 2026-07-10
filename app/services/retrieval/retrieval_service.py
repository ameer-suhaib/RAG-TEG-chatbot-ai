import logging

from app.services.embeddings.embedding_service import EmbeddingService
from app.services.vector_store.qdrant_service import QdrantService
from app.services.processing.language_detector import LanguageDetector
from app.services.retrieval.models import RetrievalResult, RetrivedChunks
from app.services.vector_store.qdrant_service import QdrantService


logger = logging.getLogger(__name__)


class RetrievalService:
    def __init__(self):
        self.embeddings = EmbeddingService()
        self.qdrant = QdrantService()
        self.language_detector = LanguageDetector()


    def retrieve(self, question: str, top_k : int = 5) -> RetrievalResult:
        language = self.language_detector.detect(question)
        logger.info("Detect language: %s", language)

        #embedding
        query_vector = self.embeddings.embed(question)

        #search result
        search_result = self.qdrant.search(
            query_vector=query_vector,
            language=language,
            limit=top_k,
        )

        chunks = []
        for point in search_result.points:
            payload = point.payload
            print(payload,"--payloadd")

            chunks.append(
                RetrivedChunks(
                    chunk_id=payload["chunk_id"],
                    content=payload['content'],
                    score=point.score,
                    url=payload['url'],
                    title=payload['title'],
                    language=payload['language'],
                    chunk_index=payload['chunk_index']
                )
            )

        logger.info("Retrived %s chunks", len(chunks))

        return RetrievalResult(
            query=question,
            language=language,
            chunks=chunks,
        )