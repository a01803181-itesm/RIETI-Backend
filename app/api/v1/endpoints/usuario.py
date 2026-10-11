"""Endpoints de gestión y verificación para la entidad de Usuario (Ciudadano)."""

from typing import Any
from asyncmy import Connection as MySQLConnection
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from app.core.db_connection import get_db
from app.schemas.usuario import Usuario, CheckEmail
from app.crud.usuario import select_user, select_all_users, insert_user

router = APIRouter()

@router.get(
    "/{user_email}",
    response_model=Usuario,
    summary="Obtener usuario por correo",
    description="Recupera la información básica de registro de un usuario ciudadano mediante su correo electrónico.",
    responses={
        status.HTTP_200_OK: {
            "model": Usuario,
            "description": "Usuario ciudadano localizado exitosamente."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No existe ningún usuario registrado con el correo electrónico proporcionado."
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "El formato del correo electrónico proporcionado en la ruta es inválido."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar la base de datos."
        }
    }
)
async def read_user_by_email(
    user_email: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Consulta y devuelve los datos de un usuario ciudadano a partir de su correo electrónico.

    Args:
        user_email (EmailStr): Correo electrónico del usuario a buscar.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Modelo Usuario con el correo y proveedor registrado.

    Raises:
        HTTPException: Con código 404 (NOT FOUND) si el usuario no existe en la base de datos.
    """
    user = await select_user(db, user_email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {user_email} not found."
        )

    return user

@router.get(
    "",
    response_model=list[Usuario],
    summary="Listar todos los usuarios",
    description="Recupera el listado completo de todos los usuarios ciudadanos registrados en la plataforma.",
    responses={
        status.HTTP_200_OK: {
            "model": list[Usuario],
            "description": "Colección de usuarios ciudadanos obtenida exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar los registros en base de datos."
        }
    }
)
async def read_all_users(db: MySQLConnection = Depends(get_db)) -> Any:
    """Recupera la lista total de usuarios ciudadanos registrados.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de modelos Usuario registrados.

    Raises:
        None.
    """
    users = await select_all_users(db)
    return users

@router.post(
    "",
    response_model=Usuario,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Inserta un nuevo usuario ciudadano asociando su proveedor de identidad federada (Cognito o Google).",
    responses={
        status.HTTP_201_CREATED: {
            "model": Usuario,
            "description": "Usuario registrado exitosamente en la plataforma."
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "No se pudo crear el usuario. Verifique si el correo ya ha sido registrado previamente."
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Datos de entrada no válidos según el esquema del usuario."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error crítico durante la transacción en base de datos."
        }
    }
)
async def register_new_user(
    user: Usuario,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Registra a un nuevo usuario ciudadano en el sistema y confirma la transacción.

    Args:
        user (Usuario): Modelo Pydantic con el correo y proveedor del usuario.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: El modelo Usuario recién registrado.

    Raises:
        HTTPException: Con código 400 (BAD REQUEST) si la inserción fue rechazada o ya existe el usuario.
    """
    new_user = await insert_user(db, user)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User could not be created. Verify the data or if the user has already been registered"
        )

    await db.commit()

    return new_user

@router.get(
    "/check-email/{email}",
    response_model=CheckEmail,
    summary="Verificar existencia de correo",
    description="Comprueba si un correo ya se encuentra registrado y retorna su proveedor de autenticación asociado para orientar el flujo de login o registro.",
    responses={
        status.HTTP_200_OK: {
            "model": CheckEmail,
            "description": "Resultado de la comprobación con flag booleano 'exists' y 'provider' asociado si existe."
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Formato de correo electrónico inválido."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar la base de datos."
        }
    }
)
async def check_user_existance(
    email: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Verifica si un correo electrónico ciudadano ya se encuentra registrado y retorna su proveedor.

    Args:
        email (EmailStr): Correo electrónico a verificar en el sistema.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Modelo CheckEmail con exists=True/False y el proveedor correspondiente.

    Raises:
        None.
    """
    user = await select_user(db, email)

    if not user:
        return CheckEmail(exists=False, provider=None)
    else:
        return CheckEmail(exists=True, provider=user.proveedor)