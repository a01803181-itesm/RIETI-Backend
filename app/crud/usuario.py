from pydantic import EmailStr
from asyncmy import Connection as MySQLAsyncConnection
import logging
from app.schemas.usuario import PublicUsuario, Usuario
from app.core.logs import LogType, log

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def select_user(conn: MySQLAsyncConnection, userEmail: EmailStr) -> PublicUsuario | None:
    query = """
        SELECT correoU
        FROM Usuario
        WHERE correoU = %s;
    """
    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (userEmail,))

            row = await cur.fetchone()

            if row:
                log(LogType.SUCCESS, f"User with email {userEmail} successfully found and fetched from DB")
                return PublicUsuario(
                    correoU=row[0]
                )

            log(LogType.WARNING, f"Could not find any user with email: {userEmail}")
            return None
    except Exception as e:
        log(LogType.ERROR, f"Error reading user with email: {userEmail}: {e}")
        return None

async def select_all_users(conn: MySQLAsyncConnection) -> list[PublicUsuario]:
    query = """
        SELECT correoU
        FROM Usuario;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                log(LogType.SUCCESS, "Select all users query successfully returned rows")
                return [
                    PublicUsuario(
                        correoU=row[0]
                    )
                    for row in rows
                ]

            log(LogType.WARNING, "User entity is empty")
            return []
    except Exception as e:
        log(LogType.ERROR, f"Error reading all users: {e}")

async def insert_user(conn: MySQLAsyncConnection, user: Usuario) -> PublicUsuario | None:
    query = """
        INSERT INTO Usuario
        (correoU, contrasenia)
        VALUES (%s, %s);
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (user.correoU, user.contrasenia))

            if cur.rowcount == 1:
                log(LogType.SUCCESS, f"User with email {user.correoU} successfully registered")
                return PublicUsuario(correoU=user.correoU)

            log(LogType.ERROR, "New user insertion failed or affected 0 rows")
            return None
    except Exception as e:
        log(LogType.ERROR, f"Error during new user insertion: {e}")
        return None