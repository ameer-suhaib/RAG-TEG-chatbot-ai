from re import S
from pydantic import BaseModel

class RetrivedChunks(BaseModel):
    chunk_id : str
    content : str
    score : float

    url : str
    title: str
    language : str
    chunk_index : int


class RetrievalResult(BaseModel):
    query : str
    language : str

    chunks : list[RetrivedChunks]