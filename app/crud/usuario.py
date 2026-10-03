from pydantic import EmailStr
from asyncmy import Connection as MySQLAsyncConnection
from app.schemas.usuario import Usuario
from app.core.logs import logger, SUCCESS
from app.schemas.enums import Provider

async def select_user(conn: MySQLAsyncConnection, userEmail: EmailStr) -> Usuario | None:
    query = """
        SELECT correoU, proveedor
        FROM Usuario
        WHERE correoU = %s;
    """
    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (userEmail,))

            row = await cur.fetchone()

            if row:
                logger.log(SUCCESS, f"User with email {userEmail} successfully found and fetched from DB")
                return Usuario(
                    correoU=row[0],
                    proveedor=Provider(row[1])
                )

            logger.warning(f"Could not find any user with email: {userEmail}")
            return None
    except Exception as e:
        logger.error(f"Error reading user with email: {userEmail}: {e}")
        return None

async def select_all_users(conn: MySQLAsyncConnection) -> list[Usuario]:
    query = """
        SELECT correoU, proveedor
        FROM Usuario;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                for row in rows:
                    print(row)
                logger.log(SUCCESS, "Select all users query successfully returned rows")
                return [
                    Usuario(
                        correoU=row[0],
                        proveedor=Provider(row[1])
                    )
                    for row in rows
                ]

            logger.warning("User entity is empty")
            return []
    except Exception as e:
        logger.error(f"Error reading all users: {e}")
        return []

async def insert_user(conn: MySQLAsyncConnection, user: Usuario) -> Usuario | None:
    query = """
        INSERT INTO Usuario
        (correoU, proveedor)
        VALUES (%s, %s);
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query,
                (user.correoU,
                user.proveedor.value)
            )

            if cur.rowcount == 1:
                logger.log(SUCCESS, f"User with email {user.correoU} successfully registered")
                return user

            logger.error("New user insertion failed or affected 0 rows")
            return None
    except Exception as e:
        logger.error(f"Error during new user insertion: {e}")
        return None