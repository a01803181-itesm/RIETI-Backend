from asyncmy import Connection as MySQLConnection
from pydantic import EmailStr
from app.schemas.reporte import Reporte
from app.core.logs import logger, SUCCESS

async def get_reporte_by_folio(conn: MySQLConnection, folio: str) -> Reporte | None:
    query = """
        SELECT
        folio, edad, dia, tipoTrabajo, numNinios, direccion, municipio,
        latitud, longitud, nombre, ap_paterno, ap_materno, detalles_adcionales,
        correoU, folioE, correoAl
        FROM Reporte
        WHERE folio = %s;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (folio,))
            row = await cur.fetchone()

            if row:
                logger.log(SUCCESS, f"Reporte with folio {folio} successfully found and fetched")
                return Reporte(
                    folio=row[0],
                    edad=row[1],
                    dia=row[2],
                    tipoTrabajo=row[3],
                    numNinios=row[4],
                    direccion=row[5],
                    municipio=row[6],
                    latitud=float(row[7]),
                    longitud=float(row[8]),
                    nombre=row[9],
                    ap_paterno=row[10],
                    ap_materno=row[11],
                    detalles_adcionales=row[12],
                    correoU=row[13],
                    folioE=row[14],
                    correoAl=row[15]
                )

            logger.warning(f"Reporte with folio {folio} not found")
            return None
    except Exception as e:
        logger.error(f"Error finding reporte with folio {folio}: {e}")
        return None


async def get_all_reportes(conn: MySQLConnection) -> list[Reporte]:
    query = """
        SELECT
        folio, edad, dia, tipoTrabajo, numNinios, direccion, municipio,
        latitud, longitud, nombre, ap_paterno, ap_materno, detalles_adcionales,
        correoU, folioE, correoAl
        FROM Reporte;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, "All reportes rows were successfully fetched and returned")
                return [
                    Reporte(
                        folio=row[0],
                        edad=row[1],
                        dia=row[2],
                        tipoTrabajo=row[3],
                        numNinios=row[4],
                        direccion=row[5],
                        municipio=row[6],
                        latitud=float(row[7]),
                        longitud=float(row[8]),
                        nombre=row[9],
                        ap_paterno=row[10],
                        ap_materno=row[11],
                        detalles_adcionales=row[12],
                        correoU=row[13],
                        folioE=row[14],
                        correoAl=row[15]
                    )
                    for row in rows
                ]

            logger.warning("'Reporte' DB entity is empty")
            return []
    except Exception as e:
        logger.error(f"Error fetching rows from 'Reporte' DB entity: {e}")
        return []


async def insert_new_reporte(conn: MySQLConnection, reporte: Reporte) -> Reporte | None:
    query = """
        INSERT INTO Reporte
        (folio, edad, dia, tipoTrabajo, numNinios, direccion, municipio,
        latitud, longitud, nombre, ap_paterno, ap_materno, detalles_adcionales,
        correoU, folioE, correoAl)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (
                reporte.folio,
                reporte.edad,
                reporte.dia,
                reporte.tipoTrabajo,
                reporte.numNinios,
                reporte.direccion,
                reporte.municipio.value,
                float(reporte.latitud),
                float(reporte.longitud),
                reporte.nombre,
                reporte.ap_paterno,
                reporte.ap_materno,
                reporte.detalles_adcionales,
                reporte.correoU,
                reporte.folioE,
                reporte.correoAl
            ))

            if cur.rowcount == 1:
                logger.log(SUCCESS, "Reporte successfully inserted into DB")
                return reporte

            logger.error("Error inserting a new Reporte. Assert that you are not trying to insert the same folio back again")
            return None
    except Exception as e:
        logger.error(f"Error during reporte insertion: {e}")
        return None