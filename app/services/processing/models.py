from datetime import datetime
from re import S
from pydantic import BaseModel, HttpUrl

class ProcessedChunk(BaseModel):
    """
    Represent a single embedding-ready chunk.
    """
    chunk_id :str
    content : str
    url : HttpUrl
    title : str | None = None
    language : str
    chunk_index : int
    crawled_at : datetime


class ProcessedChunkDocument(BaseModel):
    """
    Represent all processed chunks for one webpage.
    """
    url : HttpUrl
    title : str | None = None
    language : str
    total_chunk : int
    chunks : list[ProcessedChunk]