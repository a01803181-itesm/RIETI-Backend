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
    async with db_manager.get_connection() as conn:
        yield conn