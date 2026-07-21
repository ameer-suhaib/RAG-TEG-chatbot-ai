"""LangSmith observability setup.

LangChain / LangGraph auto-send traces when the LANGSMITH_* env vars are set.
Call ``setup_langsmith()`` once at process start, before chat / graph imports run.
"""

import logging
import os

from app.core.config import settings

logger = logging.getLogger(__name__)


def setup_langsmith() -> None:
    """Enable LangSmith tracing from Settings (copies values into os.environ)."""
    if not settings.LANGSMITH_TRACING:
        logger.info("LangSmith tracing is disabled")
        return

    if not settings.LANGSMITH_API_KEY:
        logger.warning(
            "LANGSMITH_TRACING=true but LANGSMITH_API_KEY is missing — tracing skipped"
        )
        return

    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT
    os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT

    # Older LangChain code paths still read the LANGCHAIN_* aliases.
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_API_KEY", settings.LANGSMITH_API_KEY)
    os.environ.setdefault("LANGCHAIN_PROJECT", settings.LANGSMITH_PROJECT)
    os.environ.setdefault("LANGCHAIN_ENDPOINT", settings.LANGSMITH_ENDPOINT)

    logger.info(
        "LangSmith tracing enabled (project=%s)",
        settings.LANGSMITH_PROJECT,
    )
