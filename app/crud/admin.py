from pydantic import EmailStr
from asyncmy import Connection as MySQLConnection
from app.schemas.admin import Admin
from app.core.logs import logger, SUCCESS
from app.schemas.enums import Provider

async def get_admin(conn: MySQLConnection, admin_email: EmailStr) -> Admin | None:
    query = """
        SELECT
            correoAd, proveedor, nombre,
            ap_paterno, ap_materno, telefono
        FROM Admin
        WHERE correoAd = %s;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (admin_email,))

            row = await cur.fetchone()

            if row:
                logger.log(SUCCESS, f"Admin with email {admin_email} successfully found and fetched from DB")
                return Admin(
                    correoAd=row[0],
                    proveedor=Provider(row[1]),
                    nombre=row[2],
                    ap_paterno=row[3],
                    ap_materno=row[4],
                    telefono=row[5]
                )

            logger.warning(f"Admin with email {admin_email} not found")
            return None
    except Exception as e:
        logger.error(f"Error during fetching Admin with email {admin_email}: {e}")
        return None

async def get_all_admins(conn: MySQLConnection) -> list[Admin]:
    query = """
        SELECT
            correoAd, proveedor, nombre,
            ap_paterno, ap_materno, telefono
        FROM Admin;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, f"Query successfully found Admin rows")
                return [
                    Admin(
                        correoAd=row[0],
                        proveedor=Provider(row[1]),
                        nombre=row[2],
                        ap_paterno=row[3],
                        ap_materno=row[4],
                        telefono=row[5],
                    )
                    for row in rows
                ]

            logger.warning(f"DB Entity 'Admin' has no rows")
            return []
    except Exception as e:
        logger.error(f"Error during fetching all Admin rows from DB: {e}")
        return []

async def insert_new_admin(conn: MySQLConnection, admin: Admin) -> Admin | None:
    query = """
        INSERT INTO Admin
            (correoAd, proveedor, nombre,
            ap_paterno, ap_materno, telefono)
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (
                    admin.correoAd,
                    admin.proveedor.value,
                    admin.nombre,
                    admin.ap_paterno,
                    admin.ap_materno,
                    admin.telefono,
                )
            )

            if cur.rowcount == 1:
                logger.log(SUCCESS, "Admin successfully inserted into 'Admin' entity")
                return Admin(
                    correoAd=admin.correoAd,
                    proveedor=admin.proveedor,
                    nombre=admin.nombre,
                    ap_paterno=admin.ap_paterno,
                    ap_materno=admin.ap_materno,
                    telefono=admin.telefono
                )

            logger.error("New admin insertion failed or affected 0 rows")
            return None
    except Exception as e:
        logger.error(f"Error during new admin insertion: {e}")
        return None