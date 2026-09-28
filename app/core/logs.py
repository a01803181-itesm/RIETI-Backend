import logging
from enum import Enum

logger = logging.getLogger(__name__)

class LogType(str, Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"

def log(type: LogType, content: str) -> None:
    match type:
        case LogType.INFO:
            logger.info(f'\x1b[36m[INFO]\x1b[0m - {content}')
        case LogType.SUCCESS:
            logger.info(f"\x1b[32m[SUCCESS]\x1b[0m - {content}")
        case LogType.WARNING:
            logger.warning(f"\x1b[33m[WARNING]\x1b[0m - {content}")
        case LogType.ERROR:
            logger.error(f"\x1b[31m[ERROR]\x1b[0m - {content}")
        case _:
            logger.info(f"\x1b[30m[UNKNOWN]\x1b[0m - {content}")