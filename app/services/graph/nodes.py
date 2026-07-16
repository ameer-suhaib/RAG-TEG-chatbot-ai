"""Graph node implementations for the RAG chat pipeline."""

import asyncio
import logging

from langchain_core.messages import AIMessage, HumanMessage

from app.services.citation.citation_service import CitationService
from app.services.graph.state import ChatState
from app.services.llm.llm_service import LLMService
from app.services.retrieval.prompt_builder import PromptBuilder
from app.services.retrieval.retrieval_service import RetrievalService

logger = logging.getLogger(__name__)

# How many prior turns to send to the LLM (keeps prompts bounded).
MAX_HISTORY_MESSAGES = 10


class GraphNodes:
    """Node callables wired into the LangGraph workflow (and reused for streaming)."""

    def __init__(self) -> None:
        self.retrieval = RetrievalService()
        self.prompt_builder = PromptBuilder()
        self.llm = LLMService()
        self.citation_service = CitationService()

    async def retrieval_node(self, state: ChatState) -> dict:
        """Embed the question (with light prior context) and fetch top chunks from Qdrant."""
        question = state["messages"][-1].content
        prior_user = [
            m.content
            for m in state["messages"][:-1]
            if isinstance(m, HumanMessage) and isinstance(m.content, str)
        ]
        # Include the previous user message so follow-ups retrieve better.
        search_query = (
            f"{prior_user[-1]}\n{question}" if prior_user else question
        )

        logger.info(
            "Retrieve: %d messages in thread; query=%s",
            len(state["messages"]),
            str(search_query)[:200],
        )

        # Embedding + Qdrant are blocking — keep them off the event loop.
        retrieval_result = await asyncio.to_thread(
            self.retrieval.retrieve,
            search_query,
            5,
        )
        return {
            "retrieval_result": retrieval_result.model_dump(mode="json"),
            "chunks": [
                chunk.model_dump(mode="json")
                for chunk in retrieval_result.chunks
            ],
        }

    def prompt_node(self, state: ChatState) -> dict:
        """Build system + user prompts from the question and retrieved chunks."""
        system_prompt, user_prompt = self.prompt_builder.build(
            question=state["messages"][-1].content,
            chunks=state.get("chunks") or [],
        )
        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
        }

    async def llm_node(self, state: ChatState) -> dict:
        """Call the LLM with prompts + recent history; append the AI reply to messages."""
        history = state["messages"][:-1][-MAX_HISTORY_MESSAGES:]
        logger.info("LLM: %d prior messages from thread memory", len(history))
        answer = await self.llm.generate(
            system_prompt=state["system_prompt"],
            user_prompt=state["user_prompt"],
            history=history,
        )
        return {"messages": AIMessage(content=answer)}

    def citation_node(self, state: ChatState) -> dict:
        """Deduplicate retrieved chunks into citation objects for the API response."""
        citations = self.citation_service.build(state.get("chunks") or [])
        return {
            "citations": [c.model_dump(mode="json") for c in citations],
        }
