import logging
from typing import Any

from app.services.chat.models import Citation

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
        chunks: list[Any],
    ) -> list[Citation]:

        citations: list[Citation] = []
        seen_urls: set[str] = set()

        for chunk in chunks:
            if isinstance(chunk, dict):
                url = str(chunk["url"])
                title = chunk["title"]
            else:
                url = str(chunk.url)
                title = chunk.title

            if url in seen_urls:
                continue

            seen_urls.add(url)

            citations.append(
                Citation(
                    title=title,
                    url=url,
                )
            )

        logger.info(
            "Generated %d unique citations.",
            len(citations),
        )

        return citations