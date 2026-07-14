import logging

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_openai import ChatOpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY,
        )

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        history: list[BaseMessage] | None = None,
    ) -> str:
        """
        Generate an answer.

        History is passed as real chat messages so the model
        can resolve follow-ups and remember user-stated facts.
        """
        logger.info(
            "Sending prompt to LLM with %d history messages",
            len(history or []),
        )

        messages: list[BaseMessage] = [
            SystemMessage(content=system_prompt),
        ]

        for message in history or []:
            if isinstance(message, (HumanMessage, AIMessage)):
                content = message.content
                if not isinstance(content, str):
                    content = str(content)
                # Keep history compact so RAG context stays the focus
                if isinstance(message, AIMessage) and len(content) > 500:
                    content = content[:500] + "..."
                messages.append(message.__class__(content=content))

        messages.append(HumanMessage(content=user_prompt))

        response = await self.llm.ainvoke(messages)
        logger.info("LLM response received.")
        return response.content.strip()
