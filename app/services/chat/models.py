from pydantic import BaseModel, HttpUrl


class ChatRequest(BaseModel):
    question : str


class Citation(BaseModel):
    title : str
    url : HttpUrl


class ChatResponse(BaseModel):
    answer : str
    citations : list[Citation]