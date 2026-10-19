"""Módulo de operaciones CRUD para la entidad de Administrador en MySQL."""

from pydantic import EmailStr
from asyncmy import Connection as MySQLConnection
from app.schemas.admin import Admin
from app.core.logs import logger, SUCCESS
from app.schemas.enums import Provider

async def get_admin(conn: MySQLConnection, admin_email: EmailStr) -> Admin | None:
    """Busca y recupera un administrador en la base de datos a partir de su correo electrónico.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.
        admin_email (EmailStr): Correo electrónico del administrador a consultar.

    Returns:
        Admin | None: Instancia de Admin si el registro existe en la base de datos, o None si no se encontró.

    Raises:
        Exception: Si ocurre un error de comunicación o fallo durante la ejecución de la consulta SQL.
    """
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
    """Obtiene la lista completa de todos los administradores registrados en el sistema.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        list[Admin]: Lista de objetos Admin recuperados, o una lista vacía si no existen registros.

    Raises:
        Exception: Si se produce un error durante la ejecución de la consulta a la base de datos.
    """
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
    """Inserta un nuevo registro de administrador en la tabla Admin de MySQL.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.
        admin (Admin): Modelo Pydantic con los datos del administrador a insertar.

    Returns:
        Admin | None: El objeto Admin insertado en caso de éxito, o None si la operación no afectó filas.

    Raises:
        Exception: Si ocurre un error de clave duplicada, restricción de integridad o fallo en la transacción.
    """
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

async def insert_comentario_admin(
    conn: MySQLConnection,
    correo_ad: str,
    folio: str,
    descripcion: str
) -> bool:
    query = """
        INSERT INTO AdminReporte (correoAd, folio, descripcion)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);
    """

    async with conn.cursor() as cur:
        await cur.execute(query, (correo_ad, folio, descripcion))
    return True