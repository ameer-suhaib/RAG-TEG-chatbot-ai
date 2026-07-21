"""Chat orchestration: non-streaming and token-streaming RAG replies."""

import logging
from collections.abc import AsyncIterator

from langchain_core.messages import AIMessage, HumanMessage
from langsmith import trace

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
    def _config(thread_id: str, *, run_name: str) -> dict:
        """LangGraph / LangSmith runnable config for a chat turn."""
        return {
            "configurable": {"thread_id": thread_id},
            "run_name": run_name,
            "tags": ["teg", "rag", run_name],
            "metadata": {"thread_id": thread_id},
        }

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Run retrieve → prompt → LLM → citation via the graph; return final answer."""
        config = self._config(request.thread_id, run_name="rag_chat")
        logger.info("Chat (non-stream) thread_id=%s", request.thread_id)

        # Checkpointer loads prior messages for this thread_id automatically.
        # LangGraph run is auto-traced when LangSmith env vars are set.
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

        Flow:
            1. Load prior messages from InMemorySaver (by thread_id)
            2. retrieval_node → prompt_node
            3. Yield LLM tokens to the client
            4. Checkpoint this turn (``as_node`` required — avoids Ambiguous update)

        Wrapped in a LangSmith parent trace so the stream path shows as one run tree
        (retrieve / prompt / LLM) even though it bypasses ``graph.ainvoke``.
        """
        config = self._config(request.thread_id, run_name="rag_stream_chat")

        with trace(
            name="rag_stream_chat",
            run_type="chain",
            inputs={
                "question": request.question,
                "thread_id": request.thread_id,
            },
            tags=["teg", "rag", "stream"],
            metadata={"thread_id": request.thread_id},
        ) as run:
            snapshot = await self.graph.aget_state(config)
            prior = (
                list(snapshot.values.get("messages", []))
                if snapshot.values
                else []
            )
            logger.info(
                "Stream chat thread=%s prior_messages=%d",
                request.thread_id,
                len(prior),
            )

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
                config=config,
            ):
                full_answer += token
                yield token

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

            run.outputs = {
                "answer": full_answer,
                "chars": len(full_answer),
            }
            logger.info(
                "Stream done thread=%s chars=%d",
                request.thread_id,
                len(full_answer),
            )
