"""Endpoints analíticos y de gestión para reportes de trabajo infantil."""

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from asyncmy import Connection as MySQLConnection

from app.crud import reporte
from app.crud.reporte import get_reporte_by_folio, get_all_reportes, insert_new_reporte, get_all_reportes_with_status
from app.crud.reporte import get_coordenadas_reportes, get_porcentaje_reportes_en_proceso, get_porcentaje_reportes_pendientes, get_promedio_de_resolucion
from app.crud.reporte import get_reportes_pendientes_ultima_semana, get_reportes_por_autoridad, get_reportes_por_municipio, get_reportes_por_status
from app.crud.reporte import get_reportes_por_tiempo, get_reportes_rango_hora, get_cantidad_reportes_por_estatus_especifico, get_cantidad_reportes_por_estatus
from app.crud.reporte import get_conteo_expedientes_por_municipio, get_reportes_por_tiempo_por_alimentador,get_reportes_rango_hora_por_alimentador
from app.crud.reporte import get_coordenadas_reportes_por_alimentador, get_promedio_de_resolucion_por_alimentador,get_reportes_pendientes_ultima_semana_por_alimentador
from app.crud.reporte import get_porcentaje_reportes_en_proceso_por_alimentador,get_porcentaje_reportes_pendientes_por_alimentador
from app.schemas.reporte import Reporte, CoordenadaReporte, CategoriaTotal, CantidadReportes, Data, DataInt, ReportePublic, ReporteConEstatus
from app.core.db_connection import get_db

router = APIRouter()

@router.get(
    "/estadisticas/fecha",
    response_model=list[CategoriaTotal],
    summary="Estadísticas de reportes por mes",
    description="Devuelve el agrupamiento y conteo acumulado de reportes ciudadanos según el mes en que fueron registrados.",
    responses={
        status.HTTP_200_OK: {
            "model": list[CategoriaTotal],
            "description": "Distribución mensual de reportes obtenida exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar las estadísticas en la base de datos."
        }
    }
)
async def read_reportes_por_fecha(db: MySQLConnection = Depends(get_db)) -> Any:
    """Consulta la cantidad de incidentes reportados agrupados por mes.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de diccionarios con claves 'categoria' (mes) y 'total' (número de reportes).

    Raises:
        None.
    """
    reportes = await get_reportes_por_tiempo(db)
    return [{"categoria": c, "total": t} for c, t in reportes]

@router.get(
    "/estadisticas/municipio",
    response_model=list[CategoriaTotal],
    summary="Estadísticas de reportes por municipio",
    description="Calcula y entrega el total de incidentes reportados desglosados territorialmente por cada municipio.",
    responses={
        status.HTTP_200_OK: {
            "model": list[CategoriaTotal],
            "description": "Distribución municipal de reportes obtenida exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar las estadísticas municipales."
        }
    }
)
async def read_reportes_por_municipio(db: MySQLConnection = Depends(get_db)) -> Any:
    """Calcula el total de reportes clasificados por demarcación municipal.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de diccionarios con claves 'categoria' (municipio) y 'total' (cantidad).

    Raises:
        None.
    """
    reportes = await get_reportes_por_municipio(db)
    return [{"categoria": c, "total": t} for c, t in reportes]

@router.get(
    "/estadisticas/por-rango-hora",
    response_model=list[CategoriaTotal],
    summary="Estadísticas de reportes por rango de hora",
    description="Agrupa y cuantifica los reportes de incidentes ocurridos de acuerdo con la hora del día en que se suscitaron.",
    responses={
        status.HTTP_200_OK: {
            "model": list[CategoriaTotal],
            "description": "Frecuencia horaria de reportes obtenida exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al procesar los rangos horarios."
        }
    }
)
async def read_reportes_por_rango_hora(db: MySQLConnection = Depends(get_db)) -> Any:
    """Consulta la distribución horaria (0 a 23 hrs) de la ocurrencia de los reportes.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de diccionarios con claves 'categoria' (hora) y 'total' (cantidad).

    Raises:
        None.
    """
    reportes = await get_reportes_rango_hora(db)
    return [{"categoria": c, "total": t} for c, t in reportes]

@router.get(
    "/estadisticas/por-autoridad",
    response_model=list[CategoriaTotal],
    summary="Estadísticas de reportes por autoridad",
    description="Obtiene el conteo total de reportes canalizados o atendidos por cada autoridad o alimentador registrado.",
    responses={
        status.HTTP_200_OK: {
            "model": list[CategoriaTotal],
            "description": "Distribución de carga de trabajo por autoridad obtenida exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar las estadísticas de autoridades."
        }
    }
)
async def read_reportes_por_autoridad(db: MySQLConnection = Depends(get_db)) -> Any:
    """Recupera el volumen de reportes gestionados por cada autoridad o funcionario alimentador.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de diccionarios con claves 'categoria' (nombre de la autoridad) y 'total'.

    Raises:
        None.
    """
    reportes = await get_reportes_por_autoridad(db)
    return [{"categoria": c, "total": t} for c, t in reportes]

@router.get(
    "/mapa-calor",
    response_model=list[CoordenadaReporte],
    summary="Coordenadas para mapa de calor",
    description="Extrae los pares de latitud y longitud de todos los reportes geolocalizados para alimentar componentes cartográficos y capas de calor.",
    responses={
        status.HTTP_200_OK: {
            "model": list[CoordenadaReporte],
            "description": "Listado de coordenadas geográficas obtenido exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al recuperar las coordenadas."
        }
    }
)
async def read_coordenadas_mapa(db: MySQLConnection = Depends(get_db)) -> Any:
    """Extrae las coordenadas de latitud y longitud de los reportes para mapas geoespaciales.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de objetos CoordenadaReporte con 'lat' y 'lng'.

    Raises:
        None.
    """
    coordenadas = await get_coordenadas_reportes(db)
    return [{"lat": lat, "lng": lng} for lat, lng in coordenadas]

@router.get(
    "/estadisticas/por-estatus",
    response_model=list[CategoriaTotal],
    summary="Estadísticas de reportes por estatus",
    description="Agrupa el número de expedientes y reportes según su estatus administrativo dentro del flujo de atención.",
    responses={
        status.HTTP_200_OK: {
            "model": list[CategoriaTotal],
            "description": "Distribución cuantitativa de reportes por estatus obtenida con éxito."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al clasificar los reportes por estatus."
        }
    }
)
async def read_reportes_por_estatus(db: MySQLConnection = Depends(get_db)) -> Any:
    """Obtiene la distribución del número de expedientes según su estado actual.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de diccionarios con claves 'categoria' (estatus) y 'total'.

    Raises:
        None.
    """
    data = await get_reportes_por_status(db)
    return [{"categoria": c, "total": t} for c, t in data]

@router.get(
    "/estadisticas/por-estatus/{estatus}",
    summary="Conteo por estatus específico",
    description="Consulta la cantidad total de reportes asociados a un estado particular del expediente (ej. 1_Registrado, 5_Concluido).",
    responses={
        status.HTTP_200_OK: {
            "description": "Conteo total de reportes vinculados al estatus especificado.",
            "content": {
                "application/json": {
                    "example": 24
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No se encontraron reportes vinculados al estatus proporcionado."
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Parámetro de estatus no válido."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al ejecutar la consulta."
        }
    }
)
async def read_reportes_por_estatus_especifico(
    estatus: str,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Recupera la suma de reportes correspondientes al estatus administrativo solicitado.

    Args:
        estatus (str): Cadena identificadora del estatus (ej. '1_Registrado').
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Entero con la cantidad de reportes encontrados.

    Raises:
        HTTPException: Con código 404 (NOT FOUND) si no se hallan registros para dicho estatus.
    """
    reportes = await get_cantidad_reportes_por_estatus_especifico(db, estatus)

    if not reportes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Count of reports with status {estatus} not found"
        )
    
    return reportes

@router.get(
    "/estadisticas/promedio-resolucion",
    response_model=Data,
    summary="Promedio de días de resolución",
    description="Calcula el promedio en días transcurridos desde el momento del registro hasta la conclusión formal de los casos resueltos.",
    responses={
        status.HTTP_200_OK: {
            "model": Data,
            "description": "Promedio de días de resolución calculado exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al calcular el promedio de resolución."
        }
    }
)
async def read_promedio_resolucion(db: MySQLConnection = Depends(get_db)) -> Any:
    """Calcula el promedio de días que tardan los reportes en pasar a estatus concluido.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Objeto Data con el valor decimal del promedio de resolución.

    Raises:
        None.
    """
    data = await get_promedio_de_resolucion(db)
    return {"data": data}

@router.get(
    "/estadisticas/pendientes-ultima-semana",
    response_model=DataInt,
    summary="Reportes pendientes de la última semana",
    description="Devuelve el número de reportes pendientes de resolución generados durante los últimos 7 días.",
    responses={
        status.HTTP_200_OK: {
            "model": DataInt,
            "description": "Total de reportes pendientes de los últimos 7 días obtenido exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar la métrica en la base de datos."
        }
    }
)
async def read_pendientes_ultima_semana(db: MySQLConnection = Depends(get_db)) -> Any:
    """Consulta la cantidad de incidentes reportados en la última semana que siguen pendientes de conclusión.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Objeto DataInt con el número entero de reportes pendientes.

    Raises:
        None.
    """
    data = await get_reportes_pendientes_ultima_semana(db)
    return {"data": data}

@router.get(
    "/pendientes",
    response_model=Data,
    summary="Porcentaje de reportes pendientes",
    description="Calcula la proporción porcentual de reportes que se encuentran en espera de atención ('1_Registrado' o '2_En_revision') respecto al total.",
    responses={
        status.HTTP_200_OK: {
            "model": Data,
            "description": "Porcentaje de casos pendientes calculado exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al calcular el porcentaje."
        }
    }
)
async def read_porcentaje_pendientes(db: MySQLConnection = Depends(get_db)) -> Any:
    """Calcula el porcentaje de casos sin atender respecto al universo total de reportes.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Objeto Data con el valor porcentual (0.0 a 100.0).

    Raises:
        None.
    """
    data = await get_porcentaje_reportes_pendientes(db)
    return {"data": data}

@router.get(
    "/en-proceso",
    response_model=Data,
    summary="Porcentaje de reportes en proceso",
    description="Calcula el porcentaje de reportes que actualmente están en fase de seguimiento activo ('3_En_seguimiento').",
    responses={
        status.HTTP_200_OK: {
            "model": Data,
            "description": "Porcentaje de reportes en seguimiento obtenido exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al calcular el porcentaje en proceso."
        }
    }
)
async def read_porcentaje_en_proceso(db: MySQLConnection = Depends(get_db)) -> Any:
    """Calcula la proporción porcentual de reportes actualmente bajo diligencias o visitas de campo.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Objeto Data con el porcentaje de casos en proceso.

    Raises:
        None.
    """
    data = await get_porcentaje_reportes_en_proceso(db)
    return {"data": data}

@router.get(
    "",
    response_model=list[Reporte],
    summary="Listar todos los reportes",
    description="Recupera la lista exhaustiva de todos los reportes de presunto trabajo infantil registrados en la plataforma.",
    responses={
        status.HTTP_200_OK: {
            "model": list[Reporte],
            "description": "Listado de reportes obtenido exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno de servidor al consultar los reportes."
        }
    }
)
async def read_all_reportes(db: MySQLConnection = Depends(get_db)) -> Any:
    """Recupera la totalidad de reportes ciudadanos archivados en el sistema.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de modelos Reporte con toda su información detallada.

    Raises:
        None.
    """
    reportes = await get_all_reportes(db)
    return reportes

@router.post(
    "",
    response_model=Reporte,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo reporte de trabajo infantil",
    description="Registra un nuevo incidente ciudadano con geolocalización, rangos de edad, tipología de actividad laboral y datos de contacto.",
    responses={
        status.HTTP_201_CREATED: {
            "model": Reporte,
            "description": "Reporte registrado y persistido exitosamente en el sistema."
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Datos de entrada inválidos (ej. coordenadas fuera de rango, fecha errónea)."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error al insertar el reporte en la base de datos (ej. folio duplicado o llaves foráneas inexistentes)."
        }
    }
)
async def create_new_reporte(
    reporte: Reporte,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Inserta y guarda un nuevo reporte ciudadano en la base de datos.

    Args:
        reporte (Reporte): Modelo Pydantic con la información integral del nuevo reporte a registrar.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: El modelo Reporte guardado satisfactoriamente.

    Raises:
        HTTPException: Con código 500 (INTERNAL SERVER ERROR) si ocurre un fallo al insertar o si no es único el folio.
    """
    new_reporte = await insert_new_reporte(db, reporte)

    if not new_reporte:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inserting reporte. Verify whether the folio is unique or foreign keys exist in DB."
        )

    return new_reporte

@router.get(
    "/{folio}",
    response_model=Reporte,
    summary="Obtener reporte por folio",
    description="Busca y devuelve la información completa de un reporte específico a partir de su folio alfanumérico identificador.",
    responses={
        status.HTTP_200_OK: {
            "model": Reporte,
            "description": "Reporte localizado exitosamente."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No existe ningún reporte registrado con el folio solicitado."
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Identificador de folio no procesable."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar la base de datos."
        }
    }
)
async def read_reporte_by_folio(
    folio: str,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Consulta la información detallada de un reporte utilizando su folio como identificador.

    Args:
        folio (str): Código alfanumérico único del reporte.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Modelo Reporte con los datos completos del incidente.

    Raises:
        HTTPException: Con código 404 (NOT FOUND) si el reporte no existe.
    """
    reporte_obj = await get_reporte_by_folio(db, folio)

    if not reporte_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte with folio {folio} not found"
        )

    return reporte_obj

@router.get(
    "/by-user/{user_email}",
    response_model=list[ReportePublic],
    summary="Listar reportes creados por un usuario",
    description="Obtiene el historial de todos los reportes levantados por un usuario ciudadano identificado por su correo electrónico.",
    responses={
        status.HTTP_200_OK: {
            "model": list[Reporte],
            "description": "Historial de reportes vinculados al usuario obtenido exitosamente."
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Formato de correo electrónico inválido."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar el historial del usuario."
        }
    }
)
async def read_all_reportes_made_by_user(
    user_email: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Recupera la lista de reportes emitidos históricamente por un ciudadano.

    Args:
        user_email (EmailStr): Correo electrónico del usuario consultado.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de modelos Reporte creados por dicho correo.

    Raises:
        None.
    """
    reportes = await reporte.select_all_reportes_by_user_email(db, user_email)
    return reportes

@router.get(
    "/por-estatus/cantidad",
    response_model=CantidadReportes,
    summary="Métricas consolidadas de reportes",
    description="Proporciona una vista cuantitativa consolidada con las métricas de reportes totales, completados, en proceso y pendientes para tableros directivos.",
    responses={
        status.HTTP_200_OK: {
            "model": CantidadReportes,
            "description": "Métricas consolidadas calculadas exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al calcular las métricas consolidadas."
        }
    }
)
async def read_cantidad_reportes_por_estatus(db: MySQLConnection = Depends(get_db)) -> Any:
    """Entrega los conteos consolidados de reportes por categorías de atención para paneles de control.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Objeto CantidadReportes con total, completados, en_proceso y pendientes.

    Raises:
        None.
    """
    data = await get_cantidad_reportes_por_estatus(db)
    return data

@router.get(
    "/detalles/estatus",
    response_model=list[ReporteConEstatus],
    summary="Listar todos los reportes",
    description="Recupera la lista exhaustiva de todos los reportes de presunto trabajo infantil registrados en la plataforma con su estatus.",
    responses={
        status.HTTP_200_OK: {
            "model": list[ReporteConEstatus],
            "description": "Listado de reportes obtenido exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno de servidor al consultar los reportes."
        }
    }
)
async def read_all_reportes_con_estado(db: MySQLConnection = Depends(get_db)) -> Any:
    """Recupera la totalidad de reportes ciudadanos archivados en el sistema.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de modelos Reporte con toda su información detallada.

    Raises:
        None.
    """
    reportes = await get_all_reportes_with_status(db)
    return reportes

@router.get(
    "/estadisticas/estatus-por-alimentador/{correo_al}",
    response_model=list[CategoriaTotal],
    summary="Estadísticas de estatus por municipio del alimentador",
    description="Calcula el conteo de expedientes por estatus filtrando únicamente por el municipio asociado al alimentador recibido.",
    responses={
        status.HTTP_200_OK: {
            "model": list[CategoriaTotal],
            "description": "Distribución por estatus para el municipio del alimentador obtenida exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar las estadísticas en la base de datos."
        }
    }
)
async def read_estatus_por_municipio_alimentador(
    correo_al: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Obtiene el desglose de expedientes por estatus limitados al municipio del alimentador.

    Args:
        correo_al (EmailStr): Correo electrónico del alimentador que consulta.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de diccionarios con claves 'categoria' (estatus) y 'total' (conteo).

    Raises:
        None.
    """
    data = await get_conteo_expedientes_por_municipio(db, correo_al)
    return [{"categoria": c, "total": t} for c, t in data]

@router.get(
    "/estadisticas/fecha-por-alimentador/{correo_al}",
    response_model=list[CategoriaTotal],
    summary="Estadísticas de reportes por mes según municipio del alimentador",
    description="Devuelve el conteo mensual de reportes filtrados únicamente por el municipio asignado al alimentador.",
    responses={
        status.HTTP_200_OK: {
            "model": list[CategoriaTotal],
            "description": "Distribución mensual de reportes por municipio obtenida exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar las estadísticas en la base de datos."
        }
    }
)
async def read_reportes_por_fecha_alimentador(
    correo_al: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Consulta la cantidad de incidentes reportados agrupados por mes para el municipio del alimentador.

    Args:
        correo_al (EmailStr): Correo electrónico del alimentador.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de diccionarios con claves 'categoria' (mes) y 'total' (número de reportes).

    Raises:
        None.
    """
    reportes = await get_reportes_por_tiempo_por_alimentador(db, correo_al)
    return [{"categoria": c, "total": t} for c, t in reportes]


@router.get(
    "/estadisticas/por-rango-hora-por-alimentador/{correo_al}",
    response_model=list[CategoriaTotal],
    summary="Estadísticas de reportes por rango de hora según municipio del alimentador",
    description="Agrupa y cuantifica los reportes según la hora del día en que se suscitaron, filtrando únicamente por el municipio asignado al alimentador.",
    responses={
        status.HTTP_200_OK: {
            "model": list[CategoriaTotal],
            "description": "Frecuencia horaria de reportes obtenida exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al procesar los rangos horarios."
        }
    }
)

async def read_reportes_por_rango_hora_alimentador(
    correo_al: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Consulta la distribución horaria de los reportes para el municipio del alimentador.

    Args:
        correo_al (EmailStr): Correo electrónico del alimentador que consulta.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de diccionarios con claves 'categoria' (hora) y 'total' (cantidad).

    Raises:
        None.
    """
    reportes = await get_reportes_rango_hora_por_alimentador(db, correo_al)
    return [{"categoria": c, "total": t} for c, t in reportes]

@router.get(
    "/mapa-calor/por-alimentador/{correo_al}",
    response_model=list[CoordenadaReporte],
    summary="Coordenadas para mapa de calor según municipio del alimentador",
    description="Extrae los pares de latitud y longitud de los reportes geolocalizados del municipio asignado al alimentador.",
    responses={
        status.HTTP_200_OK: {
            "model": list[CoordenadaReporte],
            "description": "Listado de coordenadas geográficas obtenido exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al recuperar las coordenadas."
        }
    }
)
async def read_coordenadas_mapa_alimentador(
    correo_al: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Extrae las coordenadas de latitud y longitud de los reportes pertenecientes al municipio del alimentador.

    Args:
        correo_al (EmailStr): Correo electrónico del alimentador que consulta.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de objetos CoordenadaReporte con 'lat' y 'lng'.

    Raises:
        None.
    """
    coordenadas = await get_coordenadas_reportes_por_alimentador(db, correo_al)
    return [{"lat": lat, "lng": lng} for lat, lng in coordenadas]

@router.get(
    "/estadisticas/promedio-resolucion/por-alimentador/{correo_al}",
    response_model=Data,
    summary="Promedio de días de resolución por municipio del alimentador",
    description="Calcula el promedio en días transcurridos desde el registro hasta la conclusión de los casos resueltos, del municipio del alimentador.",
    responses={
        status.HTTP_200_OK: {
            "model": Data,
            "description": "Promedio de días de resolución calculado exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al calcular el promedio de resolución."
        }
    }
)
async def read_promedio_resolucion_alimentador(
    correo_al: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Calcula el promedio de días que tardan los reportes en concluir para el municipio del alimentador.

    Args:
        correo_al (EmailStr): Correo electrónico del alimentador que consulta.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Objeto Data con el valor float del promedio de resolución.

    Raises:
        None.
    """
    data = await get_promedio_de_resolucion_por_alimentador(db, correo_al)
    return {"data": data}


@router.get(
    "/estadisticas/pendientes-ultima-semana/por-alimentador/{correo_al}",
    response_model=DataInt,
    summary="Reportes pendientes de la última semana por municipio del alimentador",
    description="Devuelve el número de reportes pendientes de resolución creados en los últimos 7 días en el municipio del alimentador.",
    responses={
        status.HTTP_200_OK: {
            "model": DataInt,
            "description": "Total de reportes pendientes de los últimos 7 días obtenido exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar la métrica en la base de datos."
        }
    }
)
async def read_pendientes_ultima_semana_alimentador(
    correo_al: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Consulta la cantidad de incidentes reportados en la última semana pendientes de conclusión para el municipio del alimentador.

    Args:
        correo_al (EmailStr): Correo electrónico del alimentador que consulta.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Objeto DataInt con el número entero de reportes pendientes.

    Raises:
        None.
    """
    data = await get_reportes_pendientes_ultima_semana_por_alimentador(db, correo_al)
    return {"data": data}

@router.get(
    "/en-proceso/por-alimentador/{correo_al}",
    response_model=Data,
    summary="Porcentaje de reportes en proceso por municipio del alimentador",
    description="Calcula el porcentaje de reportes que actualmente están en fase de seguimiento activo ('3_En_seguimiento') dentro del municipio del alimentador.",
    responses={
        status.HTTP_200_OK: {
            "model": Data,
            "description": "Porcentaje de reportes en seguimiento obtenido exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al calcular el porcentaje en proceso."
        }
    }
)
async def read_porcentaje_en_proceso_alimentador(
    correo_al: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Calcula la proporción porcentual de reportes en seguimiento para el municipio del alimentador.

    Args:
        correo_al (EmailStr): Correo electrónico del alimentador que consulta.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Objeto Data con el porcentaje de casos en proceso.

    Raises:
        None.
    """
    data = await get_porcentaje_reportes_en_proceso_por_alimentador(db, correo_al)
    return {"data": data}

@router.get(
    "/pendientes/por-alimentador/{correo_al}",
    response_model=Data,
    summary="Porcentaje de reportes pendientes por municipio del alimentador",
    description="Calcula la proporción porcentual de reportes que se encuentran en espera de atención ('1_Registrado' o '2_En_revision') respecto al total del municipio del alimentador.",
    responses={
        status.HTTP_200_OK: {
            "model": Data,
            "description": "Porcentaje de casos pendientes calculado exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al calcular el porcentaje."
        }
    }
)
async def read_porcentaje_pendientes_alimentador(
    correo_al: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Calcula el porcentaje de casos sin atender respecto al total de reportes del municipio del alimentador.

    Args:
        correo_al (EmailStr): Correo electrónico del alimentador que consulta.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Objeto Data con el valor porcentual (0.0 a 100.0).

    Raises:
        None.
    """
    data = await get_porcentaje_reportes_pendientes_por_alimentador(db, correo_al)
    return {"data": data}