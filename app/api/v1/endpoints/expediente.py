from fastapi import APIRouter, Depends, HTTPException, status
from asyncmy import Connection as MySQLConnection
from typing import Any
from app.schemas.expediente import Expediente
from app.core.db_connection import get_db
from app.crud.expediente import get_expediente_by_folio, get_all_expedientes, insert_new_expediente

router = APIRouter()

@router.get("/{folio}", response_model=Expediente)
async def read_expediente_by_folio(
    folio: str,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    expediente = await get_expediente_by_folio(db, folio)

    if not expediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expediente with folio {folio} not found"
        )

    return expediente

@router.get("", response_model=list[Expediente])
async def read_all_expedientes(db: MySQLConnection = Depends(get_db)) -> Any:
    expedientes = await  get_all_expedientes(db)

    return expedientes

@router.post("", response_model=Expediente, status_code=status.HTTP_201_CREATED)
async def create_new_expediente(
    expediente: Expediente,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    new_expediente = await insert_new_expediente(db, expediente)

    if not new_expediente:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inserting expediente with folio {expediente.folioE}. Verify whether the expediente has already been registered"
        )

    return new_expediente