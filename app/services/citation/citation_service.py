import logging

from app.services.chat.models import Citation
from app.services.processing.models import ProcessedChunk

logger = logging.getLogger(__name__)


class CitationService:
    """
    Builds structured citations from retrieved chunks.

    Responsibilities
    ----------------
    - Remove duplicate citations
    - Preserve retrieval order
    - Return structured citation objects
    """

    def build(
        self,
        chunks: list[ProcessedChunk],
    ) -> list[Citation]:

        citations: list[Citation] = []
        seen_urls: set[str] = set()

        for chunk in chunks:

            url = str(chunk.url)

            if url in seen_urls:
                continue

            seen_urls.add(url)

            citations.append(
                Citation(
                    title=chunk.title,
                    url=url,
                )
            )

        logger.info(
            "Generated %d unique citations.",
            len(citations),
        )

        return citations