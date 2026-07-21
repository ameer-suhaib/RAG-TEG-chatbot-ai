from datetime import datetime
from optparse import Option
from typing import Optional
from pydantic import BaseModel, HttpUrl


class CrawledPage(BaseModel):
    """
    Represented a successfully crawled webpage
    """
    url : HttpUrl
    title : Optional[str] = None
    markdown : Optional[str] = None
    html : Optional[str] = None
    status_code : int
    success : bool
    crawled_at : datetime
    filename: str | None = None
    document_type: str = "html"
