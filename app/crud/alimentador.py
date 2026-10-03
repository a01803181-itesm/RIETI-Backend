from asyncmy import Connection as MySQLConnection
from pydantic import EmailStr
from app.schemas.alimentador import Alimentador
from app.core.logs import logger, SUCCESS
from app.schemas.enums import Provider

async def get_alimentador(conn: MySQLConnection, alim_email: EmailStr) -> Alimentador | None:
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