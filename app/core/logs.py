import logging

SUCCESS = 60

logging.addLevelName(SUCCESS, "SUCCESS")

class ColouredFormatter(logging.Formatter):
    COLOURS = {
        logging.INFO: "\x1b[36m",
        logging.WARNING: "\x1b[33m",
        logging.ERROR: "\x1b[31m",
        SUCCESS: "\x1b[32m" 
    }
    RESET = "\x1b[0m"

    def format(self, record):
        colour = self.COLOURS.get(record.levelno, self.RESET)
        record.levelname = f"{colour}{record.levelname}{self.RESET}"
        record.msg = f"{colour}{record.msg}{self.RESET}"
        return super().format(record)

handler = logging.StreamHandler()
handler.setFormatter(ColouredFormatter("[%(levelName)s] %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[handler])

logger = logging.getLogger(__name__)