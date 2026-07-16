"""Chat orchestration: non-streaming and token-streaming RAG replies."""

import logging
from collections.abc import AsyncIterator

from langchain_core.messages import AIMessage, HumanMessage

from app.services.chat.models import ChatRequest, ChatResponse, Citation
from app.services.graph.nodes import GraphNodes, MAX_HISTORY_MESSAGES
from app.services.graph.workflow import build_graph

logger = logging.getLogger(__name__)


class ChatService:
    """Runs the LangGraph RAG pipeline and keeps per-thread conversation memory."""

    def __init__(self) -> None:
        self.graph = build_graph()
        # Same node implementations as the compiled graph — reused for streaming.
        self.nodes = GraphNodes()

    @staticmethod
    def _config(thread_id: str) -> dict:
        return {"configurable": {"thread_id": thread_id}}

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Run retrieve → prompt → LLM → citation via the graph; return final answer."""
        config = self._config(request.thread_id)
        logger.info("Chat (non-stream) thread_id=%s", request.thread_id)

        # Checkpointer loads prior messages for this thread_id automatically.
        result = await self.graph.ainvoke(
            {"messages": [HumanMessage(content=request.question)]},
            config=config,
        )
        return ChatResponse(
            answer=result["messages"][-1].content,
            citations=[Citation(**c) for c in result.get("citations", [])],
        )

    async def stream_chat(self, request: ChatRequest) -> AsyncIterator[str]:
        """Stream answer tokens, then persist the completed turn in the checkpointer.

        The compiled graph's LLM node returns a full string, so for token streaming
        we run retrieve → prompt → LLM.stream outside the graph, then write the
        finished human/AI messages back with ``aupdate_state``.

        Flow:
            1. Load prior messages from InMemorySaver (by thread_id)
            2. retrieval_node → prompt_node
            3. Yield LLM tokens to the client
            4. Checkpoint this turn (``as_node`` required — avoids Ambiguous update)
        """
        config = self._config(request.thread_id)

        snapshot = await self.graph.aget_state(config)
        prior = list(snapshot.values.get("messages", [])) if snapshot.values else []
        logger.info(
            "Stream chat thread=%s prior_messages=%d",
            request.thread_id,
            len(prior),
        )

        # Working state for this turn (not yet written to the checkpointer).
        state = {
            "messages": prior + [HumanMessage(content=request.question)],
        }
        state.update(await self.nodes.retrieval_node(state))
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

        # Persist as the `llm` node (the graph node that normally writes messages).
        # as_node is required when the checkpoint is empty or last writer is ambiguous.
        await self.graph.aupdate_state(
            config,
            {
                "messages": [
                    HumanMessage(content=request.question),
                    AIMessage(content=full_answer),
                ],
            },
            as_node="llm",
        )
        logger.info(
            "Stream done thread=%s chars=%d",
            request.thread_id,
            len(full_answer),
        )
