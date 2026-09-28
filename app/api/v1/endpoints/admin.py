from asyncmy import Connection as MySQLConnection
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from typing import Any
from app.core.db_connection import get_db
from app.schemas.admin import PublicAdmin, Admin
from app.crud.admin import get_admin, get_all_admins, insert_new_admin
from app.schemas.enums import Provider

router = APIRouter()

@router.get("/{admin_email}", response_model=PublicAdmin)
async def read_admin_by_email(
    admin_email: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    admin = await get_admin(db, admin_email)

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with email {admin_email} not found"
        )
    
    return admin

@router.get("", response_model=list[PublicAdmin])
async def read_all_admins(db: MySQLConnection = Depends(get_db)) -> Any:
    admins = await get_all_admins(db)
    return admins

@router.post("", response_model=PublicAdmin, status_code=status.HTTP_201_CREATED)
async def create_new_admin(
    admin: Admin,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    if admin.proveedor == Provider.GOOGLE and admin.contrasenia:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="POST /admins body request MUST NOT contain 'contrasenia' attribute when the admin is being provided by Google"
        )
    if admin.proveedor == Provider.LOCAL and admin.contrasenia is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="POST /admins body request MUST contain 'contrasenia' attribute when the admin is being provided locally"
        )

    new_admin = await insert_new_admin(db, admin)

    if not new_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin could not be created. Verify the data or if the admin has already been registered"
        )

    await db.commit()

    return new_admin