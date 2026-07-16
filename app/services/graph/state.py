"""LangGraph shared state for one chat turn / thread."""

from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ChatState(TypedDict):
    """State passed between graph nodes.

    messages:
        Conversation history. ``add_messages`` appends new messages instead of
        replacing the list (required for multi-turn memory).
    chunks:
        Retrieved chunk payloads used by prompt + citation nodes.
    citations:
        Structured sources produced by the citation node.
    retrieval_result:
        Full retrieval metadata from the retrieve node.
    system_prompt / user_prompt:
        Built by the prompt node and consumed by the LLM node.
    """

    messages: Annotated[list[BaseMessage], add_messages]
    chunks: list[dict[str, Any]]
    citations: list[dict[str, Any]]
    retrieval_result: Any
    system_prompt: str
    user_prompt: str
