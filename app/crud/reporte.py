"""Módulo de operaciones CRUD y consultas analíticas para la entidad Reporte en MySQL."""

from asyncmy import Connection as MySQLConnection
from pydantic import EmailStr
from pydantic_extra_types.coordinate import Latitude, Longitude
from app.schemas.reporte import Reporte, CantidadReportes, ReportePublic, ReporteConEstatus
from app.schemas.expediente import Expediente, Status
from app.schemas.enums import RangoEdad, TipoTrabajo
from app.core.logs import logger, SUCCESS

from fastapi import HTTPException, status

async def get_reporte_by_folio(conn: MySQLConnection, folio: str) -> Reporte | None:
    """Recupera la información completa de un reporte ciudadano mediante su identificador de folio.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.
        folio (str): Código alfanumérico único del reporte.

    Returns:
        Reporte | None: Instancia de Reporte con todos sus campos poblados si existe, o None si no fue encontrado.

    Raises:
        Exception: Si ocurre un error al ejecutar la consulta SQL o procesar los resultados.
    """
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
                    edad=RangoEdad(row[1]),
                    dia=row[2],
                    tipoTrabajo=TipoTrabajo(row[3]),
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

# async def get_all_reportes(conn: MySQLConnection) -> list[Reporte]:
#     """Obtiene la lista completa de todos los reportes de trabajo infantil registrados en la plataforma.

#     Args:
#         conn (MySQLConnection): Conexión activa a la base de datos MySQL.

#     Returns:
#         list[Reporte]: Lista de instancias de Reporte, o una lista vacía si no hay registros.

#     Raises:
#         Exception: Si ocurre un error de comunicación o fallo en la consulta.
#     """
#     query = """
#         SELECT
#             folio, edad, dia, tipoTrabajo, numNinios, direccion, municipio,
#             latitud, longitud, nombre, ap_paterno, ap_materno, detalles_adcionales,
#             correoU, folioE, correoAl
#         FROM Reporte;
#     """

#     try:
#         async with conn.cursor() as cur:
#             await cur.execute(query)
#             rows = await cur.fetchall()

#             if len(rows) > 0:
#                 logger.log(SUCCESS, "All reportes rows were successfully fetched and returned")
#                 lista = []
#                 for row in rows:
#                     lista.append(
#                         Reporte(
#                             folio=row[0],
#                             edad=RangoEdad(row[1]),
#                             dia=row[2],
#                             tipoTrabajo=TipoTrabajo(row[3]),
#                             numNinios=row[4],
#                             direccion=row[5],
#                             municipio=row[6],
#                             latitud=float(row[7]),
#                             longitud=float(row[8]),
#                             nombre=row[9],
#                             ap_paterno=row[10],
#                             ap_materno=row[11],
#                             detalles_adcionales=row[12],
#                             correoU=row[13],
#                             folioE=row[14],
#                             correoAl=row[15]
#                         )
#                     )
#                 return lista

#             logger.warning("'Reporte' DB entity is empty")
#             return []
#     except Exception as e:
#         logger.error(f"Error fetching rows from 'Reporte' DB entity: {e}")
#         return []
#         # raise e


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

            if not rows:
                return []

            lista = []
            for i, row in enumerate(rows):
                try:
                    # Intenta construir cada reporte
                    lista.append(
                        Reporte(
                            folio=row[0],
                            edad=RangoEdad(row[1]),
                            dia=row[2],
                            tipoTrabajo=TipoTrabajo(row[3]),
                            numNinios=row[4],
                            direccion=row[5],
                            municipio=row[6],
                            latitud=float(row[7]) if row[7] is not None else 0.0,
                            longitud=float(row[8]) if row[8] is not None else 0.0,
                            nombre=row[9],
                            ap_paterno=row[10],
                            ap_materno=row[11],
                            detalles_adcionales=row[12],
                            correoU=row[13],
                            folioE=row[14],
                            correoAl=row[15]
                        )
                    )
                except Exception as row_error:
                    # Si falla una fila en específico, nos dirá cuál fue y con qué datos
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Fallo en la fila {i} con datos {row}: {type(row_error).__name__} - {str(row_error)}"
                    )
            return lista

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error general en la consulta SQL: {type(e).__name__} - {str(e)}"
        )

async def get_all_reportes_with_status(conn: MySQLConnection) -> list[ReporteConEstatus]:
    query = """
        SELECT
            folio, edad, dia, tipoTrabajo, numNinios, direccion, municipio,
            latitud, longitud, nombre, ap_paterno, ap_materno, detalles_adcionales,
            correoU, r.folioE, r.correoAl, estatus
        FROM Reporte r
        JOIN Expediente e ON e.folioE = r.folioE
        ORDER BY dia;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()

            if not rows:
                return []

            lista = []
            for i, row in enumerate(rows):
                try:
                    # Intenta construir cada reporte
                    lista.append(
                        ReporteConEstatus(
                            folio=row[0],
                            edad=RangoEdad(row[1]),
                            dia=row[2],
                            tipoTrabajo=TipoTrabajo(row[3]),
                            numNinios=row[4],
                            direccion=row[5],
                            municipio=row[6],
                            latitud=float(row[7]) if row[7] is not None else 0.0,
                            longitud=float(row[8]) if row[8] is not None else 0.0,
                            nombre=row[9],
                            ap_paterno=row[10],
                            ap_materno=row[11],
                            detalles_adcionales=row[12],
                            correoU=row[13],
                            folioE=row[14],
                            correoAl=row[15],
                            estatus=row[16]
                        )
                    )
                except Exception as row_error:
                    # Si falla una fila en específico, nos dirá cuál fue y con qué datos
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Fallo en la fila {i} con datos {row}: {type(row_error).__name__} - {str(row_error)}"
                    )
            return lista

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error general en la consulta SQL: {type(e).__name__} - {str(e)}"
        )

async def get_reportes_por_status(conn: MySQLConnection) -> list[tuple[str, int]]:
    """Calcula el total de expedientes agrupados por cada uno de sus posibles estatus administrativos.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        list[tuple[str, int]]: Lista de tuplas donde cada elemento contiene (estatus, conteo).

    Raises:
        Exception: Si ocurre un error durante el agrupamiento o la lectura de la base de datos.
    """
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


async def get_cantidad_reportes_por_estatus_especifico(conn: MySQLConnection, estatus: str) -> int:
    """Obtiene la cantidad total de reportes asociados a un estado de expediente específico.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.
        estatus (str): Nombre o clave del estatus a consultar (ej. '1_Registrado').

    Returns:
        int: Conteo total de reportes vinculados al estatus consultado.

    Raises:
        Exception: Si ocurre un error en la ejecución del JOIN o conteo en la base de datos.
    """
    query = """
        SELECT COUNT(folio)
        FROM Reporte r
        JOIN Expediente e ON e.folioE = r.folioE
        WHERE estatus = %s
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (estatus,))

            row = await cur.fetchone()

            if row:
                logger.log(SUCCESS, f"Count of reports with status {estatus} successfully fetched and returned")
                
                return int(row[0])
            logger.warning(f"No reports with status {estatus} were found")
            return 0
    except Exception as e:
        logger.error(f"Error founding reports with status {estatus}: {e}")
        return 0

async def get_reportes_por_tiempo(conn: MySQLConnection) -> list[tuple[str, int]]:
    """Agrupa y contabiliza los reportes registrados según el mes de ocurrencia.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        list[tuple[str, int]]: Lista de tuplas conformadas por (nombre_del_mes, total_reportes).

    Raises:
        Exception: Si ocurre un error al ejecutar la función MONTHNAME o agrupar los datos.
    """
    query = """
        SELECT MONTHNAME(dia), COUNT(folio)
        FROM Reporte
        GROUP BY MONTH(dia), MONTHNAME(dia);
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, "Number of reports by date succesfully fetched and returned")

                return [(str(row[0]), int(row[1])) for row in rows]
            logger.warning("No reports with date asigned were found")
            return []
    except Exception as e:
        logger.error(f"Error founding reports by date: {e}")
        return []

async def get_reportes_por_municipio(conn: MySQLConnection) -> list[tuple[str, int]]:
    """Calcula la cantidad total de reportes desglosados geográficamente por municipio.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        list[tuple[str, int]]: Lista de tuplas con el formato (municipio, total_reportes).

    Raises:
        Exception: Si falla la consulta de agregación por municipio en la base de datos.
    """
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

async def get_reportes_rango_hora(conn: MySQLConnection) -> list[tuple[str, int]]:
    """Cuantifica los incidentes reportados agrupándolos por la hora del día en que tuvieron lugar.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        list[tuple[str, int]]: Lista de tuplas conteniendo (hora_del_dia, total_reportes).

    Raises:
        Exception: Si ocurre un error al extraer la hora o agrupar la información.
    """
    query = """
        SELECT EXTRACT(HOUR FROM dia), COUNT(EXTRACT(HOUR FROM dia))
        FROM Reporte
        GROUP BY EXTRACT(HOUR FROM dia);
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, "Reports by hour successfully fetched and returned")
                return [(str(row[0]), int(row[1])) for row in rows]

            logger.warning("No reports by hour were found")
            return []
    except Exception as e:
        logger.error(f"Error founding reports by hour: {e}")
        return []

async def get_reportes_por_autoridad(conn: MySQLConnection) -> list[tuple[str, int]]:
    """Obtiene el número de reportes gestionados por cada autoridad o alimentador registrado.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        list[tuple[str, int]]: Lista de tuplas con el formato (nombre_completo_autoridad, total_reportes).

    Raises:
        Exception: Si se genera un fallo en el JOIN entre Reporte y Alimentador.
    """
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

async def get_coordenadas_reportes(conn: MySQLConnection) -> list[tuple[float, float]]:
    """Recupera los pares de coordenadas geográficas (latitud, longitud) de todos los reportes.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        list[tuple[float, float]]: Lista de tuplas con las coordenadas (latitud, longitud) en formato flotante.

    Raises:
        Exception: Si ocurre un error al consultar las coordenadas en la base de datos.
    """
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

async def get_promedio_de_resolucion(conn: MySQLConnection) -> float:
    """Calcula el tiempo promedio en días transcurrido entre el registro y la conclusión de los casos resueltos.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        float: Promedio de días para resolución de casos concluidos ('5_Concluido'), o 0.0 si no hay casos.

    Raises:
        Exception: Si ocurre un error al calcular la diferencia de fechas o el promedio SQL.
    """
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

async def get_reportes_pendientes_ultima_semana(conn: MySQLConnection) -> int:
    """Calcula la cantidad de reportes pendientes de resolución creados en los últimos 7 días.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        int: Total de reportes pendientes generados durante la última semana.

    Raises:
        Exception: Si ocurre un error durante el filtrado por fecha y estatus en la consulta.
    """
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

async def get_porcentaje_reportes_en_proceso(conn: MySQLConnection) -> float:
    """Calcula el porcentaje de reportes que se encuentran en estatus de seguimiento respecto al total global.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        float: Valor porcentual (0.0 a 100.0) de reportes con estatus '3_En_seguimiento'.

    Raises:
        Exception: Si ocurre un error en la subconsulta de porcentajes o división en MySQL.
    """
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

async def get_porcentaje_reportes_pendientes(conn: MySQLConnection) -> float:
    """Calcula el porcentaje de reportes que permanecen en estados preliminares ('1_Registrado' o '2_En_revision').

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        float: Proporción porcentual (0.0 a 100.0) de reportes pendientes frente al universo total.

    Raises:
        Exception: Si ocurre un error en la subconsulta o división por cero en la base de datos.
    """
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

async def get_cantidad_reportes_por_estatus(conn: MySQLConnection) -> CantidadReportes | None:
    """Recupera un resumen consolidado de las cantidades de reportes totales, completados, en proceso y pendientes.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.

    Returns:
        CantidadReportes | None: Objeto CantidadReportes con las 4 métricas desglosadas, o None si no se pudo consultar.

    Raises:
        Exception: Si se produce un error en la evaluación de subconsultas simultáneas.
    """
    query = """
        SELECT COUNT(folio),
            (SELECT COUNT(folio)
                FROM Reporte r
                JOIN Expediente e ON e.folioE = r.folioE
                WHERE estatus = "5_Concluido"),
            (SELECT COUNT(folio)
                            FROM Reporte r
                            JOIN Expediente e ON e.folioE = r.folioE
                            WHERE estatus = "3_En_seguimiento"
                            OR estatus = "2_En_revision"),
            (SELECT COUNT(folio)
                            FROM Reporte r
                            JOIN Expediente e ON e.folioE = r.folioE
                            WHERE estatus = "1_Registrado")
        FROM Reporte;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query)

            row = await cur.fetchone()

            if row:
                logger.log(SUCCESS, "Total amount of reports and count of reports by estatus successfully fetched and returned")
                return CantidadReportes(
                    total=row[0],
                    completados=row[1],
                    en_proceso=row[2],
                    pendientes=row[3])
            
            logger.warning("Unable to obtain the total amount of reports and the count of reports by status.")
            return None
    except Exception as e:
        logger.error(f"Error founding the total amount of reports and the count of reports by status: {e}")
        return None

async def insert_new_reporte(conn: MySQLConnection, reporte: Reporte) -> Reporte | None:
    """Inserta un nuevo registro de reporte ciudadano en la base de datos y confirma la transacción.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.
        reporte (Reporte): Modelo Pydantic con la información detallada del reporte a guardar.

    Returns:
        Reporte | None: La instancia de Reporte guardada en caso de éxito, o None si falló la inserción.

    Raises:
        Exception: Si se viola la unicidad del folio, fallan las llaves foráneas o se produce un error de conexión.
    """
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
                reporte.edad.value,
                reporte.dia,
                reporte.tipoTrabajo.value,
                reporte.numNinios,
                reporte.direccion,
                reporte.municipio,
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

async def select_all_reportes_by_user_email(conn: MySQLConnection, email: EmailStr) -> list[ReportePublic]:
    """Obtiene el historial completo de reportes creados por un usuario ciudadano específico.

    Args:
        conn (MySQLConnection): Conexión activa a la base de datos MySQL.
        email (EmailStr): Correo electrónico del usuario denunciante.

    Returns:
        list[Reporte]: Lista de reportes generados por dicho usuario, o lista vacía si no tiene reportes.

    Raises:
        Exception: Si ocurre un error al consultar los reportes del usuario en la base de datos.
    """
    query = """
        SELECT 
            r.folio, r.edad, r.dia, r.tipoTrabajo, r.numNinios,
            r.direccion, r.municipio, r.latitud, r.longitud,
            r.nombre, r.ap_paterno, r.ap_materno, r.detalles_adcionales,
            r.correoU, r.folioE, r.correoAl, e.lugar, e.descripcion, e.estatus
        FROM RIETI.Reporte r LEFT JOIN RIETI.Expediente e ON r.folioE = e.folioE
        WHERE r.correoU = %s;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(query, (email,))

            rows = await cur.fetchall()

            if len(rows) > 0:
                logger.log(SUCCESS, f"Successfully retrieved {len(rows)} reports from user with email {email}")
                reportesResponse: list[ReportePublic] = []

                for row in rows:
                    expediente: Expediente | None = None
                    reporte: Reporte = Reporte(
                        folio=row[0],
                        edad=RangoEdad(row[1]),
                        dia=row[2],
                        tipoTrabajo=TipoTrabajo(row[3]),
                        numNinios=row[4],
                        direccion=row[5],
                        municipio=row[6],
                        latitud=Latitude(row[7]),
                        longitud=Longitude(row[8]),
                        nombre=row[9],
                        ap_paterno=row[10],
                        ap_materno=row[11],
                        detalles_adcionales=row[12],
                        correoU=row[13],
                        folioE=row[14],
                        correoAl=row[15]
                    )

                    logger.info(f"FolioE: {row[14]}")
                    if row[14] != None:
                        expediente = Expediente(
                            folioE=row[14],
                            lugar=row[16],
                            descripcion=row[17],
                            status=Status(row[18]),
                            correoAl=row[15]
                        )

                    reportesResponse.append(ReportePublic(reporte=reporte, expediente=expediente))

                return reportesResponse

            logger.warning(f"There are no reports registered by user {email}")
            return []
    except Exception as e:
        logger.error(f"Error at retrieving reports linked by user {email}: {e}")
        return []