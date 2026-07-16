from typing import TypedDict, Annotated, Any

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from pydantic import BaseModel

from app.services.retrieval.models import RetrivedChunks
from app.services.chat.models import Citation

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    context: str
    # citations: list
    chunks: list[dict[str, Any]]
    citations:  list[dict[str, Any]]
    retrieval_result: Any
    system_prompt: str
    user_prompt: str



class ChatRequest(BaseModel):
    question: str
    thread_id: str