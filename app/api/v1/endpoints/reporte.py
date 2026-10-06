from pydantic import EmailStr
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from asyncmy import Connection as MySQLConnection

from app.crud import reporte
from app.crud.reporte import get_reporte_by_folio, get_all_reportes, insert_new_reporte
from app.crud.reporte import get_coordenadas_reportes, get_porcentaje_reportes_en_proceso, get_porcentaje_reportes_pendientes, get_promedio_de_resolucion, get_reportes_pendientes_ultima_semana, get_reportes_por_autoridad, get_reportes_por_municipio, get_reportes_por_status, get_reportes_por_tiempo
from app.schemas.reporte import Reporte, CoordenadaReporte, CategoriaTotal, DashboardData
from app.core.db_connection import get_db

router = APIRouter()

@router.get("/mapa-calor", response_model=list[CoordenadaReporte])
async def read_coordenadas_mapa(db: MySQLConnection = Depends(get_db)) -> Any:
    coordenadas = await get_coordenadas_reportes(db)
    return [{"lat": lat, "lng": lng} for lat, lng in coordenadas]

@router.get("/estadisticas/por-estatus", response_model=list[CategoriaTotal])
async def read_reportes_por_estatus(db: MySQLConnection = Depends(get_db)) -> Any:
    data = await get_reportes_por_status(db)
    return [{"categoria": c, "total": t} for c, t in data]

@router.get("/dashboard-data", response_model=DashboardData)
async def read_dashboard_data(db: MySQLConnection = Depends(get_db)) -> Any:
    promedio = await get_promedio_de_resolucion(db)
    pendientesUltimaSemana = await get_reportes_pendientes_ultima_semana(db)
    enProceso = await get_porcentaje_reportes_en_proceso(db)
    pendientes = await get_porcentaje_reportes_pendientes(db)

    return {
        "promedio_dias_resolucion": promedio,
        "pendientes_ultima_semana": pendientesUltimaSemana,
        "porcentaje_en_proceso": enProceso,
        "porcentaje_pendientes": pendientes,
    }

@router.get("", response_model=list[Reporte])
async def read_all_reportes(db: MySQLConnection = Depends(get_db)) -> Any:
    reportes = await get_all_reportes(db)
    return reportes

@router.post("", response_model=Reporte, status_code=status.HTTP_201_CREATED)
async def create_new_reporte(
    reporte: Reporte,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    new_reporte = await insert_new_reporte(db, reporte)

    if not new_reporte:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inserting reporte. Verify whether the folio is unique or foreign keys exist in DB."
        )

    return new_reporte


@router.get("/{folio}", response_model=Reporte)
async def read_reporte_by_folio(
    folio: str,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    reporte = await get_reporte_by_folio(db, folio)

    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte with folio {folio} not found"
        )

    return reporte

@router.get("/by-user/{user_email}", response_model=list[Reporte])
async def read_all_reportes_made_by_user(
    user_email: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    reportes = await reporte.select_all_reportes_by_user_email(db, user_email)
    return reportes