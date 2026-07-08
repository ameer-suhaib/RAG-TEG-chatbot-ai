import enum
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.crawler.models import CrawledPage
from .models import (
    ProcessedChunk,
    ProcessedChunkDocument
)
import uuid


class DocumentChunker:
    """Splits cleaned documents into embedding-ready chunks."""

    def __init__(self, chunks_size : int = 1000, chunk_overlap : int = 200):
        print(chunks_size, chunk_overlap)
        print(type(chunks_size))
        print(type(chunk_overlap),"-----typee")
        self.splitter = RecursiveCharacterTextSplitter(chunk_size= int(chunks_size), chunk_overlap = int(chunk_overlap), length_function = len)


    def chunk(self, page: CrawledPage, cleaned_text : str, language: str) -> ProcessedChunkDocument:
        texts = self.splitter.split_text(cleaned_text)
        chunks : list[ProcessedChunk] = []

        for index, text in enumerate(texts):
            # Deterministic UUID based on URL + chunk index + chunk content
            chunk_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"{page.url}|{index}|{text}",
                )
            )

            chunks.append(
                ProcessedChunk(
                    chunk_id=chunk_id,
                    content = text,
                    chunk_index=index,
                    url = page.url,
                    title = page.title,
                    language=language,
                    crawled_at = page.crawled_at
                )
            )
        return ProcessedChunkDocument(
            url= page.url,
            title = page.title,
            language=language,
            total_chunk=len(chunks),
            chunks = chunks
        )