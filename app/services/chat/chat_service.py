import logging

from langchain_core.messages import HumanMessage

from app.services.chat.models import ChatRequest, ChatResponse, Citation



from app.services.graph.workflow import build_graph

logger = logging.getLogger(__name__)


class ChatService:

    def __init__(self):
        self.graph = build_graph()


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

        # Verify checkpoint memory for this thread
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
        logger.info(
            "Thread %s now has %d total messages",
            request.thread_id,
            len(result["messages"]),
        )
        return ChatResponse(
            answer=answer,
            citations=[
                Citation(**c)
                for c in result.get("citations", [])
            ]
        )