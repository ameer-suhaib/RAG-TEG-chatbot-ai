import logging
import logging.config #pre build library
from pathlib import Path

#Create logs directory if it doesn't exist
LOG_DIR = Path("storage/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },

    "handlers": {

        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },

        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOG_FILE),
            "formatter": "default",
            "level": "INFO",
            "encoding": "utf-8",
        },
    },

    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}


def setup_logging():
    """
    Configure application logging.
    """
    logging.config.dictConfig(LOGGING_CONFIG)


