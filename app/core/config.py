from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # =====================================================
    # Application
    # =====================================================

    APP_NAME: str = "TEG AI Assistant"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # =====================================================
    # OpenAI
    # =====================================================

    OPENAI_API_KEY: str

    LLM_MODEL: str = "gpt-4.1-mini"
    LLM_TEMPERATURE: float = 0
    LLM_MAX_TOKENS: int = 1000

    # =====================================================
    # Embeddings
    # =====================================================

    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSION: int = 1536

    # =====================================================
    # Qdrant
    # =====================================================

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "teg_knowledge_base"

    # =====================================================
    # Chunking
    # =====================================================

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # =====================================================
    # Retrieval
    # =====================================================

    TOP_K: int = Field(default=5, ge=1)

    MIN_SCORE: float = Field(
        default=0.65,
        ge=0,
        le=1,
    )

    # =====================================================
    # Crawler
    # =====================================================

    USER_AGENT: str = "TEG-RAG-Crawler/1.0"

    PAGE_TIMEOUT: int = 30000

    # =====================================================
    # Refresh
    # =====================================================

    ENABLE_AUTO_REFRESH: bool = False

    REFRESH_INTERVAL_HOURS: int = 24

    # =====================================================
    # Logging
    # =====================================================

    LOG_LEVEL: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """
    Returns a singleton Settings instance.
    """
    return Settings()


settings = get_settings()