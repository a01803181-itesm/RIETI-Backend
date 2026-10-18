"""Módulo de operaciones CRUD para la entidad de Alimentador (Autoridad) en MySQL."""

from asyncmy import Connection as MySQLConnection
from pydantic import EmailStr
from app.schemas.alimentador import Alimentador
from app.core.logs import logger, SUCCESS
from app.schemas.enums import Provider

async def get_alimentador(conn: MySQLConnection, alim_email: EmailStr) -> Alimentador | None:
    """Busca y recupera una autoridad alimentadora en la base de datos a partir de su correo electrónico.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.
        alim_email (EmailStr): Correo electrónico del alimentador a consultar.

    Returns:
        Alimentador | None: Instancia de Alimentador si existe en la base de datos, o None si no se encontró.

    Raises:
        Exception: Si ocurre un error de comunicación o fallo durante la ejecución de la consulta SQL.
    """
    query = """
        SELECT
            correoAl, proveedor, telefono,
            nombre, ap_paterno, ap_materno, municipio
        FROM Alimentador
        WHERE correoAl = %s;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (alim_email,))

            row = await cur.fetchone()

            if row:
                logger.log(SUCCESS, f"Alimentador with email {alim_email} successfully found and fetched")
                return Alimentador(
                    correoAl=row[0],
                    proveedor=Provider(row[1]),
                    telefono=row[2],
                    nombre=row[3],
                    ap_paterno=row[4],
                    ap_materno=row[5],
                    municipio=row[6]
                )

            logger.warning(f"Alimentador with email {alim_email} not found")
            return None
    except Exception as e:
        logger.error(f"Error founding alimentador with email {alim_email}: {e}")
        return None

async def get_all_alimentadores(conn: MySQLConnection) -> list[Alimentador]:
    """Obtiene la lista completa de autoridades alimentadoras registradas en el sistema.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        list[Alimentador]: Lista de objetos Alimentador recuperados, o lista vacía si no existen registros.

    Raises:
        Exception: Si se produce un error durante la ejecución de la consulta a la base de datos.
    """
    query = """
        SELECT
            correoAl, proveedor, telefono,
            nombre, ap_paterno, ap_materno, municipio
        FROM Alimentador;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, f"All alimentadores rows where successfully fetched and returned")
                return [
                    Alimentador(
                        correoAl=row[0],
                        proveedor=Provider(row[1]),
                        telefono=row[2],
                        nombre=row[3],
                        ap_paterno=row[4],
                        ap_materno=row[5],
                        municipio=row[6]
                    )
                    for row in rows
                ]

            logger.warning(f"'Alimentador' DB entity is empty")
            return []
    except Exception as e:
        logger.error(f"Error during fetching rows from 'Alimentador' DB entity: {e}")
        return []

async def insert_new_alimentador(conn: MySQLConnection, alimentador: Alimentador) -> Alimentador | None:
    """Inserta una nueva autoridad alimentadora en la tabla Alimentador de MySQL.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.
        alimentador (Alimentador): Modelo Pydantic con los datos del alimentador a insertar.

    Returns:
        Alimentador | None: El objeto Alimentador insertado en caso de éxito, o None si falló la inserción.

    Raises:
        Exception: Si ocurre un error de clave duplicada, restricción de integridad o fallo en la transacción.
    """
    query = """
        INSERT INTO Alimentador
            (correoAl, proveedor, telefono,
            nombre, ap_paterno, ap_materno, municipio)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (
                    alimentador.correoAl,
                    alimentador.proveedor.value,
                    alimentador.telefono,
                    alimentador.nombre,
                    alimentador.ap_paterno,
                    alimentador.ap_materno,
                    alimentador.municipio
                )
            )

            if cur.rowcount == 1:
                logger.log(SUCCESS, "Alimentador successfully inserted into DB")
                return Alimentador(
                    correoAl=alimentador.correoAl,
                    proveedor=alimentador.proveedor,
                    telefono=alimentador.telefono,
                    nombre=alimentador.nombre,
                    ap_paterno=alimentador.ap_paterno,
                    ap_materno=alimentador.ap_materno,
                    municipio=alimentador.municipio
                )

            logger.error("Error during inserting a brand new Alimentador. Assert that you are not trying to insert the same alimentador back again")
            return None
    except Exception as e:
        logger.error(f"Error during alimentador insertion: {e}")
        return None


async def get_all_alimentadores_by_municipio(conn: MySQLConnection, municipio: str) -> list[Alimentador]:
    query = """
        SELECT
            correoAl, proveedor, telefono,
            nombre, ap_paterno, ap_materno, municipio
        FROM Alimentador
        WHERE municipio = %s;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (municipio,))

            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, f"All alimentadores rows where successfully fetched and returned")
                return [
                    Alimentador(
                        correoAl=row[0],
                        proveedor=Provider(row[1]),
                        telefono=row[2],
                        nombre=row[3],
                        ap_paterno=row[4],
                        ap_materno=row[5],
                        municipio=row[6]
                    )
                    for row in rows
                ]

            logger.warning(f"'Alimentadores' with municipio {municipio} not found")
            return []
    except Exception as e:
        logger.error(f"Error during fetching alimentadores with municipio {municipio}: {e}")
        return []