"""Módulo de conexión y administración del pool asíncrono de MySQL.

Define las estructuras de datos y el gestor de ciclo de vida del pool mediante asyncmy.
"""

from dataclasses import dataclass
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncmy
from asyncmy import Connection as AsyncMySQLConnection

@dataclass
class Connection:
    """Parámetros de conexión requeridos para autenticación y enlace al servidor MySQL.

    Attributes:
        host (str): Dirección de host o IP del servidor.
        user (str): Nombre de usuario de la base de datos.
        password (str): Contraseña del usuario.
        name (str): Nombre de la base de datos a utilizar.
        port (str): Puerto de enlace de MySQL (por defecto 3306).
    """
    host: str
    user: str
    password: str
    name: str
    port: str

class MySQLManager:
    """Administrador de ciclo de vida del pool de conexiones asíncronas a MySQL.

    Gestiona la creación, adquisición y liberación de conexiones eficientes mediante asyncmy.
    """
    __connection: Connection
    __pool: asyncmy.Pool | None

    def __init__(self, con: Connection) -> None:
        """Inicializa una nueva instancia del gestor de base de datos MySQL.

        Args:
            con (Connection): Objeto con los parámetros de conexión configurados.

        Returns:
            None
        """
        self.__connection = con
        self.__pool = None

    async def initialize(self) -> None:
        """Crea e inicializa el pool de conexiones asíncronas con autocommit activado.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: Si falla la conexión inicial o las credenciales son inválidas.
        """
        self.__pool = await asyncmy.create_pool(
            host=self.__connection.host,
            port=int(self.__connection.port),
            user=self.__connection.user,
            password=self.__connection.password,
            db=self.__connection.name,
            minsize=4,
            maxsize=50,
            autocommit=True
        )

    @property
    def pool(self) -> asyncmy.Pool | None:
        """Obtiene la instancia actual del pool de conexiones.

        Returns:
            asyncmy.Pool | None: El pool de conexiones activo o None si no ha sido inicializado.
        """
        return self.__pool

    async def close(self) -> None:
        """Cierra de manera ordenada todas las conexiones del pool y espera su liberación total.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: Si ocurre un error al intentar cerrar el pool.
        """
        if self.__pool:
            self.__pool.close()
            await self.__pool.wait_closed()

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[AsyncMySQLConnection, None]:
        """Context manager asíncrono para adquirir y liberar una conexión del pool.

        Args:
            None

        Returns:
            AsyncGenerator[AsyncMySQLConnection, None]: Generador que entrega una conexión activa.

        Raises:
            RuntimeError: Si el pool de conexiones no ha sido inicializado antes de la llamada.
        """
        if not self.__pool:
            raise RuntimeError("Database pool has not been initialized yet")

        async with self.__pool.acquire() as connection:
            yield connection