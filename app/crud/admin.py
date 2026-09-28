from pydantic import EmailStr
from asyncmy import Connection as MySQLConnection
from app.schemas.admin import Admin
from app.core.logs import LogType, log

async def get_admin(conn: MySQLConnection, admin_email: EmailStr) -> Admin | None:
    query = """
        SELECT
        correoAd, contrasenia, nombre,
        ap_paterno, ap_materno, telefono
        FROM Admin
        WHERE correoAd = %s;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            row = cur.fetchone()

            if not row:
                log(LogType.SUCCESS, f"Admin with email {admin_email} successfully found and fetched from DB")
                return Admin(
                    correoAd=row[0],
                    contrasenia=row[1],
                    nombre=row[2],
                    ap_paterno=row[3],
                    ap_materno=row[4],
                    telefono=row[5]
                )

            log(LogType.WARNING, f"Admin with email {admin_email} not found")
            return None
    except Exception as e:
        log(LogType.ERROR, f"Error during fetching Admin with email {admin_email}: {e}")
        return None

async def get_all_admins(conn: MySQLConnection) -> list[Admin]:
    query = """
        SELECT
        correoAd, contrasenia, nombre,
        ap_paterno, ap_materno, telefono
        FROM Admin;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = cur.fetchall()

            if len(rows) > 0:
                log(LogType.SUCCESS, f"Query successfully found Admin rows")
                return [
                    Admin(
                        correoAd=row[0],
                        contrasenia=row[1],
                        nombre=row[2],
                        ap_paterno=row[3],
                        ap_materno=row[4],
                        telefono=row[5],
                    )
                    for row in rows
                ]

            log(LogType.WARNING, f"DB Entity 'Admin' has no rows")
            return []
    except Exception as e:
        log(LogType.ERROR, f"Error during fetching all Admin rows from DB: {e}")
        return []