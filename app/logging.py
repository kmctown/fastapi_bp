import logging

from app.enums import StrEnum
from app.core.config import settings


LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


def configure_logging() -> None:
    log_level = str(settings.LOG_LEVEL).upper()
    log_levels = list(LogLevel)

    if log_level not in log_levels:
        logging.basicConfig(level=LogLevel.ERROR)
        return

    if log_level == LogLevel.DEBUG:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return

    logging.basicConfig(level=log_level)
