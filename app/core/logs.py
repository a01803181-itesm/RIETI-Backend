"""Módulo de configuración del sistema de bitácoras y formateo visual de logs.

Configura niveles personalizados como SUCCESS y aplica colores ANSI según la severidad del mensaje.
"""

import logging

SUCCESS = 60

logging.addLevelName(SUCCESS, "SUCCESS")

class ColouredFormatter(logging.Formatter):
    """Formateador de registros de log con soporte para colores en consola usando códigos de escape ANSI.

    Attributes:
        COLOURS (dict): Mapeo de niveles de registro de logging a secuencias de escape ANSI.
        RESET (str): Secuencia ANSI para restablecer el color de la terminal.
    """

    COLOURS = {
        logging.INFO: "\x1b[36m",
        logging.WARNING: "\x1b[33m",
        logging.ERROR: "\x1b[31m",
        SUCCESS: "\x1b[32m" 
    }
    RESET = "\x1b[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Aplica estilos de color ANSI al nombre del nivel de log y formatea el mensaje.

        Args:
            record (logging.LogRecord): Objeto con la información del evento de bitácora a emitir.

        Returns:
            str: Cadena formateada del registro con las secuencias de color correspondientes.

        Raises:
            Exception: Si ocurre un error inesperado al formatear el registro.
        """
        colour = self.COLOURS.get(record.levelno, self.RESET)
        record.levelname = f"{colour}{record.levelname}{self.RESET}"
        record.msg = f"{record.msg}"
        return super().format(record)

handler = logging.StreamHandler()
handler.setFormatter(ColouredFormatter("[%(levelname)s] %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[handler])

logger = logging.getLogger(__name__)