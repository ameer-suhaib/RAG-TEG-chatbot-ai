import asyncio
import logging
from collections.abc import AsyncIterator

from langchain_core.messages import AIMessage, HumanMessage

from app.services.chat.models import ChatRequest, ChatResponse, Citation
from app.services.graph.nodes import GraphNodes, MAX_HISTORY_MESSAGES
from app.services.graph.workflow import build_graph

logger = logging.getLogger(__name__)


class ChatService:

    def __init__(self):
        self.graph = build_graph()
        self.nodes = GraphNodes()

    async def chat(self, request: ChatRequest) -> ChatResponse:
        logger.info(
            "Starting chat pipeline for thread_id=%s",
            request.thread_id,
        )
        config = {
            "configurable": {
                "thread_id": request.thread_id
            }
        }

        existing = await self.graph.aget_state(config)
        prior_count = len(existing.values.get("messages", [])) if existing.values else 0
        logger.info(
            "Loaded %d prior messages from InMemorySaver for thread %s",
            prior_count,
            request.thread_id,
        )

        result = await self.graph.ainvoke(
            {
                "messages": [
                    HumanMessage(content=request.question)
                ]
            },
            config=config,
        )
        answer = result["messages"][-1].content
        return ChatResponse(
            answer=answer,
            citations=[
                Citation(**c)
                for c in result.get("citations", [])
            ],
        )

    async def stream_chat(self, request: ChatRequest) -> AsyncIterator[str]:
        config = {
            "configurable": {
                "thread_id": request.thread_id
            }
        }

        snapshot = await self.graph.aget_state(config)
        prior_messages = (
            list(snapshot.values.get("messages", []))
            if snapshot.values
            else []
        )
        logger.info(
            "Streaming chat for thread %s with %d prior messages",
            request.thread_id,
            len(prior_messages),
        )

        state = {
            "messages": prior_messages + [
                HumanMessage(content=request.question)
            ],
        }

        retrieval_update = await self.nodes.retrieval_node(state)
        state.update(retrieval_update)
        state.update(self.nodes.prompt_node(state))

        history = state["messages"][:-1][-MAX_HISTORY_MESSAGES:]
        full_answer = ""

        async for token in self.nodes.llm.generate_stream(
            system_prompt=state["system_prompt"],
            user_prompt=state["user_prompt"],
            history=history,
        ):
            full_answer += token
            yield token

        citations = self.nodes.citation_service.build(state.get("chunks") or [])
        citation_payload = [
            c.model_dump(mode="json")
            for c in citations
        ]

        await self.graph.aupdate_state(
            config,
            {
                "messages": [
                    HumanMessage(content=request.question),
                    AIMessage(content=full_answer),
                ],
                "chunks": state.get("chunks", []),
                "citations": citation_payload,
                "system_prompt": state.get("system_prompt", ""),
                "user_prompt": state.get("user_prompt", ""),
            },
            as_node="citation",
        )

        logger.info(
            "Stream completed for thread %s (%d chars)",
            request.thread_id,
            len(full_answer),
        )
