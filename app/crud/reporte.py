from asyncmy import Connection as MySQLConnection
from pydantic import EmailStr
from pydantic_extra_types.coordinate import Latitude, Longitude
from app.schemas.reporte import Reporte
from app.schemas.enums import MunicipioEnum
from app.core.logs import logger, SUCCESS

# OBTENER REPORTE
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
                    municipio=row[6].strip() if isinstance(row[6], str) else row[6],
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

# OBTENER REPORTES
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
                lista = []
                for row in rows:
                    lista.append(
                        Reporte(
                            folio=row[0],
                            edad=row[1],
                            dia=row[2],
                            tipoTrabajo=row[3],
                            numNinios=row[4],
                            direccion=row[5],
                            municipio=row[6].strip() if isinstance(row[6], str) else row[6],
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
                    )
                return lista

            logger.warning("'Reporte' DB entity is empty")
            return []
    except Exception as e:
        logger.error(f"Error fetching rows from 'Reporte' DB entity: {e}")
        return []

# OBTENER REPORTES POR ESTATUS
async def get_reportes_por_status(conn: MySQLConnection) -> list[tuple[str, int]]:
    query = """
        SELECT estatus, COUNT(folioE)
        FROM Expediente
        GROUP BY estatus; 
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, "Count of reports by status succesfully fetched and returned")
                
                return [(str(row[0]), int(row[1])) for row in rows]
            logger.warning("No reports with status found")
            return []
    except Exception as e:
        logger.error(f"Error founding reports with a status: {e}")
        return []

async def get_reportes_por_tiempo(conn: MySQLConnection) -> list[tuple[str, int]]:
    query = """
        SELECT 
            MONTHNAME(dia) AS mes, 
            COUNT(folio) AS total
        FROM Reporte
        WHERE dia IS NOT NULL
        GROUP BY MONTHNAME(dia), MONTH(dia)
        ORDER BY MONTH(dia) ASC;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()

            if rows:
                logger.log(SUCCESS, "Number of reports by date successfully fetched and returned")
                
                resultado = []
                for row in rows:
                    # Soporta tanto tuplas como diccionarios (DictCursor)
                    if isinstance(row, dict):
                        mes = row.get("mes") or ""
                        total = row.get("total") or 0
                    else:
                        mes = row[0] or ""
                        total = row[1] or 0
                    
                    resultado.append((str(mes), int(total)))
                
                return resultado

            logger.warning("No reports with date assigned were found")
            return []
            
    except Exception as e:
        logger.error(f"Error finding reports by date: {e}")
        # Si no capturas la excepción aquí o la relanzas, FastAPI no sabrá el detalle original
        raise e

# OBTENER REPORTES POR FECHA Y HORA
# async def get_reportes_por_tiempo(conn: MySQLConnection) -> list[tuple[str, int]]:
#     query = """
#         SELECT MONTHNAME(dia), COUNT(folio)
#         FROM Reporte
#         GROUP BY MONTH(dia), MONTHNAME(dia);
#     """

#     try:
#         async with conn.cursor() as cur:
#             await cur.execute(query)

#             rows = await cur.fetchall()

#             if len(rows) > 0:
#                 logger.log(SUCCESS, "Number of reports by date succesfully fetched and returned")

#                 return [(str(row[0]), int(row[1])) for row in rows]
#             logger.warning("No reports with date asigned were found")
#             return []
#     except Exception as e:
#         logger.error(f"Error founding reports by date: {e}")
#         return []

# OBTENER REPORTES POR MUNICIPIO
async def get_reportes_por_municipio(conn: MySQLConnection) -> list[tuple[str, int]]:
    query = """
        SELECT municipio, COUNT(folio)
        FROM Reporte
        GROUP BY municipio;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, "Reports by municipality successfully fetched and returned")

                return [(str(row[0]), int(row[1])) for row in rows]
            logger.warning("No reports by municipality were found")
            return []
    except Exception as e:
        logger.error(f"Error founding reports by municipality: {e}")
        return []

# OBTENER REPORTES POR AUTORIDAD
async def get_reportes_por_autoridad(conn: MySQLConnection) -> list[tuple[str, int]]:
    query = """
        SELECT CONCAT(a.nombre, ' ', a.ap_paterno), COUNT(r.folio)
        FROM Reporte r
        JOIN Alimentador a ON a.correoAl = r.correoAl
        GROUP BY a.correoAl, a.nombre, a.ap_paterno;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, "Reports by autority successfully fetched and returned")
                return [(str(row[0]), int(row[1])) for row in rows]
            
            logger.warning("No reports by autority were found")
            return []
    except Exception as e:
        logger.error(f"Error founding reports by autority: {e}")
        return []

# OBTENER COORDENADAS (PARA MAPA DE CALOR)
async def get_coordenadas_reportes(conn: MySQLConnection) -> list[tuple[float, float]]:
    query = """
        SELECT latitud, longitud
        FROM Reporte;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, "List of coordinates fetched and returned successfully")
                return [(float(row[0]), float(row[1])) for row in rows]

            logger.warning("Unable to obtain coordinates. No reports were found")
            return []
    except Exception as e:
        logger.error(f"Error fetching coordinates: {e}")
        return []

    
# OBTENER FECHA PROMEDIO DE RESOLUCIÓN DE REPORTES EN GENERAL (FECHA DE REGISTRO - HOY)
async def get_promedio_de_resolucion(conn: MySQLConnection) -> float:
    query = """
        SELECT COALESCE(AVG(DATEDIFF(CURDATE(), r.dia)), 0)
        FROM Reporte r
        JOIN Expediente e ON e.folioE = r.folioE
        WHERE estatus = "5_Concluido";
    """ 

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            row = await cur.fetchone()

            if row and row[0] is not None:
                logger.log(SUCCESS, "Percentage fetched and returned successfully")
                return float(row[0])

            return 0.0
    except Exception as e:
        logger.error(f"Error founding the average of resolution: {e}")
        return 0.0

# OBTENER REPORTES PENDIENTES REALIZADOS EN LA ÚLTIMA SEMANA
async def get_reportes_pendientes_ultima_semana(conn: MySQLConnection) -> int:
    query = """
        SELECT COUNT(folio)
        FROM Reporte r
        JOIN Expediente e ON e.folioE = r.folioE
        WHERE DATEDIFF(CURDATE(), dia) <= 7
        AND estatus != "5_Concluido";
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            row = await cur.fetchone()

            if row:
                logger.log(SUCCESS, "Count of pending reports made on the last seven days fetched and returned successfully")
                return int(row[0])

            logger.warning("Unable to obtain the number of pending reports of the last seven days")
            return 0
    except Exception as e:
        logger.error(f"Error founding pending reports made on the last seven days: {e}")
        return 0

# OBTENER PORCENTAJE DE REPORTES TOTALES EN PROCESO
async def get_porcentaje_reportes_en_proceso(conn: MySQLConnection) -> float:
    query = """
        SELECT 
            COALESCE(
                (SELECT COUNT(folio)
                FROM Reporte r
                JOIN Expediente e ON e.folioE = r.folioE
                WHERE estatus = "3_En_seguimiento")
                / 
                NULLIF((SELECT COUNT(folio)
                FROM Reporte), 0) * 100, 0);
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            row = await cur.fetchone()

            if row and row[0] is not None:
                logger.log(SUCCESS, "Percentage fetched and returned successfully")
                return float(row[0])

            return 0.0
    except Exception as e:
        logger.error(f"Error founding the percentage of pending reports: {e}")
        return 0.0

# OBTENER PORCENTAJE DE REPORTES TOTALES EN ESTADO PENDIENTE
async def get_porcentaje_reportes_pendientes(conn: MySQLConnection) -> float:
    query = """
        SELECT 
            COALESCE(
                (SELECT COUNT(folio)
                FROM Reporte r
                JOIN Expediente e ON e.folioE = r.folioE
                WHERE estatus = "1_Registrado"
                OR estatus = "2_En_revision")
                /
                 NULLIF((SELECT COUNT(folio)
                FROM Reporte), 0) * 100, 0);
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            row = await cur.fetchone()

            if row and row[0] is not None:
                logger.log(SUCCESS, "Percentage fetched and returned successfully")
                return float(row[0])

            return 0.0
    except Exception as e:
        logger.error(f"Error founding the percentage of reports on process: {e}")
        return 0.0

# INSERTAR NUEVO REPORTE
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
                reporte.municipio.value if hasattr(reporte.municipio, 'value') else reporte.municipio,
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
                await conn.commit()
                logger.log(SUCCESS, "Reporte successfully inserted into DB")
                return reporte

            logger.error("Error inserting a new Reporte. Assert that you are not trying to insert the same folio back again")
            return None
    except Exception as e:
        logger.error(f"Error during reporte insertion: {e}")
        return None

async def select_all_reportes_by_user_email(conn: MySQLConnection, email: EmailStr) -> list[Reporte]:
    query = """
        SELECT 
            folio, edad, dia, tipoTrabajo, numNinios,
            direccion, municipio, latitud, longitud,
            nombre, ap_paterno, ap_materno, detalles_adcionales,
            correoU, folioE, correoAl
        FROM Reporte
        WHERE correoU = %s;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (email,))

            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, f"Successfully retrieved {len(rows)} reports from user with email {email}")
                return [
                    Reporte(
                        folio=row[0],
                        edad=row[1],
                        dia=row[2],
                        tipoTrabajo=row[3],
                        numNinios=row[4],
                        direccion=row[5],
                        municipio=MunicipioEnum(row[6]),
                        latitud=Latitude(row[7]),
                        longitud=Longitude(row[8]),
                        nombre=row[9],
                        ap_paterno=row[10],
                        ap_materno=row[11],
                        detalles_adcionales=row[12],
                        correoU=row[13],
                        folioE=row[14],
                        correoAl=row[15],
                    )
                    for row in rows
                ]

            logger.warning(f"There are no reports registered by user {email}")
            return []
    except Exception as e:
        logger.error(f"Error at retrieving reports linked by user {email}: {e}")
        return []