from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from asyncmy import Connection as MySQLConnection

from app.crud.reporte import get_reporte_by_folio, get_all_reportes, insert_new_reporte
from app.schemas.reporte import Reporte
from app.core.db_connection import get_db

router = APIRouter()

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