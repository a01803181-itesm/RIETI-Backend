from asyncmy import Connection as MySQLConnection
from pydantic import EmailStr
from app.schemas.alimentador import Alimentador
from app.core.logs import LogType, log

async def get_alimentador(conn: MySQLConnection, alim_email: EmailStr) -> Alimentador | None:
    query = """
        SELECT
        correoAl, contrasenia, telefono,
        nombre, ap_paterno, ap_materno, municipio
        FROM Alimentador
        WHERE correoAl = %s;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (alim_email,))

            row = await cur.fetchone()

            if row:
                log(LogType.SUCCESS, f"Alimentador with email {alim_email} successfully found and fetched")
                return Alimentador(
                    correoAl=row[0],
                    contrasenia=row[1],
                    telefono=row[2],
                    nombre=row[3],
                    ap_paterno=row[4],
                    ap_materno=row[5],
                    municipio=row[6]
                )

            log(LogType.WARNING, f"Alimentador with email {alim_email} not found")
            return None
    except Exception as e:
        log(LogType.ERROR, f"Error founding alimentador with email {alim_email}: {e}")
        return None

async def get_all_alimentadores(conn: MySQLConnection) -> list[Alimentador]:
    query = """
        SELECT
        correoAl, contrasenia, telefono,
        nombre, ap_paterno, ap_materno, municipio
        FROM Alimentador;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                log(LogType.SUCCESS, f"All alimentadores rows where successfully fetched and returned")
                return [
                    Alimentador(
                        correoAl=row[0],
                        contrasenia=row[1],
                        telefono=row[2],
                        nombre=row[3],
                        ap_paterno=row[4],
                        ap_materno=row[5],
                        municipio=row[6]
                    )
                    for row in rows
                ]

            log(LogType.WARNING, f"'Alimentador' DB entity is empty")
            return []
    except Exception as e:
        log(LogType.ERROR, f"Error during fetching rows from 'Alimentador' DB entity: {e}")
        return []