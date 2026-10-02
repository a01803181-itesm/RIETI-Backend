from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from typing import Any
from asyncmy import Connection as MySQLConnection
from app.core.db_connection import get_db
from app.schemas.usuario import Usuario
from app.crud.usuario import select_user, select_all_users, insert_user

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

@router.post("", response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def register_new_user(
    user: Usuario,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    new_user = await insert_user(db, user)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User could not be created. Verify the data or if the user has already been registered"
        )

    await db.commit()

    return new_user