"""Endpoints de gestión y consulta para la entidad de Administrador."""

from typing import Any
from asyncmy import Connection as MySQLConnection
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from app.core.db_connection import get_db
from app.schemas.admin import Admin
from app.crud.admin import get_admin, get_all_admins, insert_new_admin

router = APIRouter()

@router.get(
    "/{admin_email}",
    response_model=Admin,
    summary="Obtener administrador por correo",
    description="Busca y recupera la información de perfil de un administrador registrado mediante su correo electrónico institucional.",
    responses={
        status.HTTP_200_OK: {
            "model": Admin,
            "description": "Administrador localizado exitosamente."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No existe ningún administrador registrado con el correo electrónico proporcionado."
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "El formato del correo electrónico proporcionado en la ruta es inválido."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar la base de datos."
        }
    }
)
async def read_admin_by_email(
    admin_email: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Consulta los datos de un administrador registrado mediante su dirección de correo electrónico.

    Args:
        admin_email (EmailStr): Correo electrónico del administrador a buscar.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Modelo Admin con la información del administrador.

    Raises:
        HTTPException: Con código 404 (NOT FOUND) si no existe ningún registro con dicho correo.
    """
    admin = await get_admin(db, admin_email)

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with email {admin_email} not found"
        )
    
    return admin

@router.get(
    "",
    response_model=list[Admin],
    summary="Listar todos los administradores",
    description="Recupera el listado completo de todos los administradores registrados en la plataforma.",
    responses={
        status.HTTP_200_OK: {
            "model": list[Admin],
            "description": "Listado de administradores obtenido exitosamente (puede ser una lista vacía)."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno de servidor o falla al consultar los registros."
        }
    }
)
async def read_all_admins(db: MySQLConnection = Depends(get_db)) -> Any:
    """Obtiene la colección de todos los administradores existentes en el sistema.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de modelos Admin registrados.

    Raises:
        None.
    """
    admins = await get_all_admins(db)
    return admins

@router.post(
    "",
    response_model=Admin,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo administrador",
    description="Crea e inserta un nuevo registro de administrador en el sistema con sus datos de contacto y credenciales.",
    responses={
        status.HTTP_201_CREATED: {
            "model": Admin,
            "description": "Administrador creado y registrado exitosamente en la base de datos."
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "No se pudo crear el administrador. Verifique si el correo ya ha sido registrado previamente."
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Datos de entrada no procesables o violación de formato en el esquema de solicitud."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error crítico durante la transacción en base de datos."
        }
    }
)
async def create_new_admin(
    admin: Admin,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Registra a un nuevo administrador en la plataforma y confirma la transacción en base de datos.

    Args:
        admin (Admin): Objeto Pydantic con los datos personales y credenciales del nuevo administrador.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: El modelo Admin recién creado y persistido.

    Raises:
        HTTPException: Con código 400 (BAD REQUEST) si la inserción falló o si el correo ya existe.
    """
    new_admin = await insert_new_admin(db, admin)

    if not new_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin could not be created. Verify the data or if the admin has already been registered"
        )

    await db.commit()

    return new_admin