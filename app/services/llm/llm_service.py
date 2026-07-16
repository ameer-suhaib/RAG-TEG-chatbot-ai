import logging
from collections.abc import AsyncIterator

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_openai import ChatOpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

_llm: ChatOpenAI | None = None


def _get_llm() -> ChatOpenAI:
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY,
        )
    return _llm


class LLMService:

    def __init__(self):
        self.llm = _get_llm()

    def _build_messages(
        self,
        system_prompt: str,
        user_prompt: str,
        history: list[BaseMessage] | None = None,
    ) -> list[BaseMessage]:
        messages: list[BaseMessage] = [
            SystemMessage(content=system_prompt),
        ]

        for message in history or []:
            if isinstance(message, (HumanMessage, AIMessage)):
                content = message.content
                if not isinstance(content, str):
                    content = str(content)
                if isinstance(message, AIMessage) and len(content) > 500:
                    content = content[:500] + "..."
                messages.append(message.__class__(content=content))

        messages.append(HumanMessage(content=user_prompt))
        return messages

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        history: list[BaseMessage] | None = None,
    ) -> str:
        logger.info(
            "Sending prompt to LLM with %d history messages",
            len(history or []),
        )
        messages = self._build_messages(system_prompt, user_prompt, history)
        response = await self.llm.ainvoke(messages)
        logger.info("LLM response received.")
        return response.content.strip()

    async def generate_stream(
        self,
        system_prompt: str,
        user_prompt: str,
        history: list[BaseMessage] | None = None,
    ) -> AsyncIterator[str]:
        logger.info(
            "Streaming prompt to LLM with %d history messages",
            len(history or []),
        )
        messages = self._build_messages(system_prompt, user_prompt, history)

        async for chunk in self.llm.astream(messages):
            token = chunk.content
            if isinstance(token, str) and token:
                yield token
            elif isinstance(token, list):
                for part in token:
                    if isinstance(part, str) and part:
                        yield part
                    elif isinstance(part, dict) and part.get("type") == "text":
                        text = part.get("text", "")
                        if text:
                            yield text

        logger.info("LLM stream completed.")
