import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import settings


def setup_logging() -> None:
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setFormatter(formatter)

    logging.basicConfig(level=settings.log_level, handlers=[console_handler, file_handler])
