from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from typing import Any
from asyncmy import Connection as MySQLConnection
from app.crud.alimentador import get_alimentador, get_all_alimentadores, insert_new_alimentador
from app.schemas.alimentador import Alimentador
from app.core.db_connection import get_db

router = APIRouter()

@router.get("/{alim_email}", response_model=Alimentador)
async def read_alimentador_by_email(
    alim_email: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    alimentador = await get_alimentador(db, alim_email)

    if not alimentador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alimentador with email {alim_email} not found"
        )

    return alimentador

@router.get("", response_model=list[Alimentador])
async def read_all_alimentadores(db: MySQLConnection = Depends(get_db)) -> Any:
    alimentadores = await get_all_alimentadores(db)
    return alimentadores

@router.post("", response_model=Alimentador, status_code=status.HTTP_201_CREATED)
async def create_new_alimentador(
    alimentador: Alimentador,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    new_alimentador = await insert_new_alimentador(db, alimentador)

    if not new_alimentador:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inserting alimentador. Verify whether the alimentador has not been registered already"
        )

    return new_alimentador