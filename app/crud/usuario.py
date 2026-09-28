from pydantic import EmailStr
from asyncmy import Connection as MySQLAsyncConnection
import logging
from app.schemas.usuario import Usuario
from app.core.logs import LogType, log

logger = logging.getLogger(__name__)

async def select_user(conn: MySQLAsyncConnection, userEmail: EmailStr) -> Usuario | None:
    query = """
        SELECT correoU, contrasenia
        FROM Usuario
        WHERE correoU = %s;
    """
    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (userEmail,))

            row = await cur.fetchone()

            if row:
                log(LogType.SUCCESS, f"User with email {userEmail} successfully found and fetched from DB")
                return Usuario(
                    correoU=row[0],
                    contrasenia=row[1]
                )

            log(LogType.WARNING, f"Could not find any user with email: {userEmail}")
            return None
    except Exception as e:
        log(LogType.ERROR, f"Error reading user with email: {userEmail}: {e}")
        return None

async def select_all_users(conn: MySQLAsyncConnection) -> list[Usuario]:
    query = """
        SELECT correoU, contrasenia
        FROM Usuario;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                log(LogType.SUCCESS, "Select all users query successfully returned rows")
                return [
                    Usuario(
                        correoU=row[0],
                        contrasenia=row[1],
                    )
                    for row in rows
                ]

            log(LogType.WARNING, "User entity is empty")
            return []
    except Exception as e:
        log(LogType.ERROR, f"Error reading all users: {e}")