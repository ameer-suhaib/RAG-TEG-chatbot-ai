import logging
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    """
    
    
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model = settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY,
        )

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate an answer from the LLM.
        Parameters
        --------
        system_prompt
            Behaviour instruction.
        user_prompt
            Prompt containing context and user question.
        Returns
        -------
        str
            Generate answer.
        
        """
        logger.info("Sening prompt to LLM..")
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = await self.llm.ainvoke(messages)
        logger.info("LLM response received.")
        return response.content.strip()