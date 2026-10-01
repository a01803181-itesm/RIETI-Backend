from asyncmy import Connection as MySQLConnection
from app.schemas.expediente import Expediente
from app.core.logs import logger, SUCCESS

async def get_expediente_by_folio(conn: MySQLConnection, folio: str) -> Expediente | None:
    query = """
        SELECT
            folioE, lugar, descripcion,
            estatus, correoAl
        FROM Expediente
        WHERE folioE = %s;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (folio,))

            row = await cur.fetchone()

            if row:
                logger.log(SUCCESS, f'Expediente with folio {folio} successfully fetched')
                return Expediente(
                    folioE=row[0],
                    lugar=row[1],
                    descripcion=row[2],
                    estatus=row[3],
                    correoAl=row[4]
                )

            logger.warning(f'Expediente with folio {folio} could not be found')
            return None
    except Exception as e:
        logger.error(f'Error during selecting expediente with folio {folio}: {e}')
        return None

async def get_all_expedientes(conn: MySQLConnection) -> list[Expediente]:
    query = """
        SELECT
            folioE, lugar, descripcion,
            estatus, correoAl
        FROM Expediente;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, "Expediente DB rows successfully fetched")
                return [
                    Expediente(
                        folioE=row[0],
                        lugar=row[1],
                        descripcion=row[2],
                        estatus=row[3],
                        correoAl=row[4]
                    )
                    for row in rows
                ]

            logger.warning("Expediente DB entity has no rows yet")
            return []
    except Exception as e:
        logger.error(f"Error during reading all expedientes: {e}")
        return []

async def insert_new_expediente(conn: MySQLConnection, expediente: Expediente) -> Expediente | None:
    query = """
        INSERT INTO Expediente
            (folioE, lugar, descripcion,
            estatus, correoAl)
        VALUES (%s, %s, %s, %s, %s);
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(
                query,
                (
                    expediente.folioE,
                    expediente.lugar,
                    expediente.descripcion,
                    expediente.estatus,
                    expediente.correoAl
                )
            )

            if cur.rowcount == 1:
                logger.log(SUCCESS, f"Expediente with folio {expediente.folioE} successfully inserted")
                return expediente

            logger.error(f"Error inserting expediente with folio {expediente.folioE}. Probably the expediente is already registered")
            return None
    except Exception as e:
        logger.error(f"Error during expediente with folio {expediente.folioE} insertion: {e}")
        return None