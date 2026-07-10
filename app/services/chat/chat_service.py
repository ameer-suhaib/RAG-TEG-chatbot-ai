import logging
from re import L

from langchain_core.messages import Citation

from app.services.chat.models import ChatRequest, ChatResponse
from app.services.citation.citation_service import CitationService
from app.services.llm.llm_service import LLMService
from app.services.retrieval.prompt_builder import PromptBuilder
from app.services.retrieval.retrieval_service import RetrievalService

logger = logging.getLogger(__name__)


class ChatService:
    """
    Orchestrates the complete RAG pipeline.

    Flow

        User Question
              │
              ▼
        Retrieval Service
              │
              ▼
        Prompt Builder
              │
              ▼
          LLM Service
              │
              ▼
       Citation Service
              │
              ▼
         Chat Response

    This class intentionally contains no business logic.
    """
    def __init__(self):
        self.retriever = RetrievalService()
        self.prompt_builder = PromptBuilder()
        self.llm = LLMService()
        self.citation_service  = CitationService()


    async def chat(self, request: ChatRequest) -> ChatResponse:
        logger.info("Starting chat pipeline")
        #retrieve relavent document
        retrieval_result = self.retriever.retrieve(
            request.question
        )
        if not retrieval_result.chunks:
            logger.warning("No relavent documemnt found")
            return ChatResponse(
                answer=(
                    "sorry i counld not find any relavent "
                    "information on the TEG website"
                ),
                citations=[]
            )
        logger.info("Retrieved %d chunks", len(retrieval_result.chunks))

        #build prompt
        system_prompt, user_prompt = self.prompt_builder.build(retrieval_result)

        #generate answer
        answer =await self.llm.generate(system_prompt, user_prompt)

        #build citation
        citations = self.citation_service.build(retrieval_result.chunks)
        logger.info(
            "Generated %d citations",
            len(citations)
        )

        #return reponse
        return ChatResponse(
            answer=answer,
            citations=citations
        )