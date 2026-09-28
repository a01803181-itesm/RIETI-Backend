from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from typing import Any
from asyncmy import Connection as MySQLConnection
from app.core.db_connection import get_db
from app.schemas.usuario import Usuario
from app.crud.usuario import select_user, select_all_users

router = APIRouter()

@router.get("/{user_email}", response_model=Usuario)
async def read_user_by_email(
    user_email: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    user = await select_user(db, user_email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {user_email} not found."
        )

    return user

@router.get("", response_model=list[Usuario])
async def read_all_users(db: MySQLConnection = Depends(get_db)) -> Any:
    users = await select_all_users(db)
    return users