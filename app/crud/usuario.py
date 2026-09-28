from pydantic import EmailStr
from asyncmy import Connection as MySQLAsyncConnection
from app.schemas.usuario import PublicUsuario, Usuario
from app.core.logs import logger, SUCCESS

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
                logger.log(SUCCESS, f"User with email {userEmail} successfully found and fetched from DB")
                return PublicUsuario(
                    correoU=row[0]
                )

            logger.warning(f"Could not find any user with email: {userEmail}")
            return None
    except Exception as e:
        logger.error(f"Error reading user with email: {userEmail}: {e}")
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
                logger.log(SUCCESS, "Select all users query successfully returned rows")
                return [
                    PublicUsuario(
                        correoU=row[0]
                    )
                    for row in rows
                ]

            logger.warning("User entity is empty")
            return []
    except Exception as e:
        logger.error(f"Error reading all users: {e}")

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
                logger.log(SUCCESS, f"User with email {user.correoU} successfully registered")
                return PublicUsuario(correoU=user.correoU)

            logger.error("New user insertion failed or affected 0 rows")
            return None
    except Exception as e:
        logger.error(f"Error during new user insertion: {e}")
        return None