from pydantic import BaseModel

class IngestionResult(BaseModel):
    page_crawled : int
    page_processed : int
    chunk_created : int
    vectors_indexed: int
    failed_pages: int