"""Módulo de gestión y dependencia de conexión a la base de datos MySQL.

Provee el generador asíncrono `get_db` para inyección de dependencias en endpoints de FastAPI,
administrando la adquisición y liberación de conexiones del pool.
"""

from typing import AsyncGenerator
from asyncmy import Connection as MySQLAsyncConnection
from dotenv import load_dotenv
from app.core.mysql import Connection, MySQLManager
from app.core.config import settings

load_dotenv()

connection: Connection = Connection(
    host=settings.MYSQL_DB_HOST,
    password=settings.MYSQL_DB_PASSWORD,
    name=settings.MYSQL_DB_NAME,
    user=settings.MYSQL_DB_USER,
    port=settings.MYSQL_DB_PORT
)

db_manager: MySQLManager = MySQLManager(connection)

async def get_db() -> AsyncGenerator[MySQLAsyncConnection, None]:
    """Generador asíncrono para inyección de dependencias de conexión a la base de datos.

    Adquiere una conexión activa del pool de MySQL durante el ciclo de vida de la petición HTTP
    y garantiza su devolución al pool al finalizar la ejecución del endpoint.

    Args:
        None.

    Returns:
        AsyncGenerator[MySQLAsyncConnection, None]: Generador asíncrono que cede una conexión activa de MySQL.

    Raises:
        RuntimeError: Si el pool de conexiones no ha sido inicializado previamente.
        Exception: Si ocurre un error al adquirir o liberar la conexión en el pool.
    """
    conn = await db_manager.pool.acquire()
    try:
        yield conn
    finally:
        db_manager.pool.release(conn)