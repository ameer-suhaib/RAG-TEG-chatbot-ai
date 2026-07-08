from pydantic import BaseModel

class IngestionResult(BaseModel):
    pages_crawled : int
    pages_processed : int
    chunks_created : int
    vectors_indexed: int
    failed_pages: int