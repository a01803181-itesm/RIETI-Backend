"""Endpoints de gestión y consulta para la entidad de Alimentador (Autoridad)."""

from typing import Any
from asyncmy import Connection as MySQLConnection
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from app.crud.alimentador import get_alimentador, get_all_alimentadores, insert_new_alimentador, get_all_alimentadores_by_municipio
from app.schemas.alimentador import Alimentador
from app.core.db_connection import get_db

router = APIRouter()

@router.get(
    "/{alim_email}",
    response_model=Alimentador,
    summary="Obtener alimentador por correo",
    description="Consulta los detalles y jurisdicción municipal de una autoridad o alimentador mediante su correo electrónico institucional.",
    responses={
        status.HTTP_200_OK: {
            "model": Alimentador,
            "description": "Alimentador localizado exitosamente."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No existe ningún alimentador registrado con el correo electrónico proporcionado."
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "El formato del correo electrónico proporcionado en la ruta es inválido."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno al consultar la base de datos."
        }
    }
)
async def read_alimentador_by_email(
    alim_email: EmailStr,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Consulta la información de perfil y municipio de una autoridad o alimentador de campo.

    Args:
        alim_email (EmailStr): Correo electrónico del alimentador a buscar.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Modelo Alimentador con los datos correspondientes.

    Raises:
        HTTPException: Con código 404 (NOT FOUND) si el alimentador no existe en el sistema.
    """
    alimentador = await get_alimentador(db, alim_email)

    if not alimentador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alimentador with email {alim_email} not found"
        )

    return alimentador

@router.get(
    "",
    response_model=list[Alimentador],
    summary="Listar todos los alimentadores",
    description="Recupera el listado completo de todas las autoridades y alimentadores registrados en el sistema.",
    responses={
        status.HTTP_200_OK: {
            "model": list[Alimentador],
            "description": "Listado de autoridades alimentadoras obtenido exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno de servidor o falla en la consulta de registros."
        }
    }
)
async def read_all_alimentadores(db: MySQLConnection = Depends(get_db)) -> Any:
    """Recupera la colección completa de alimentadores institucionales registrados.

    Args:
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: Lista de modelos Alimentador registrados.

    Raises:
        None.
    """
    alimentadores = await get_all_alimentadores(db)
    return alimentadores

@router.post(
    "",
    response_model=Alimentador,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo alimentador",
    description="Registra una nueva autoridad o funcionario de campo asignándole un municipio y datos de contacto.",
    responses={
        status.HTTP_201_CREATED: {
            "model": Alimentador,
            "description": "Alimentador registrado exitosamente en la plataforma."
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Fallo al insertar el alimentador. Verifique si el correo ya ha sido registrado previamente."
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Error de validación en la estructura o campos del alimentador enviado."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno del servidor durante la transacción en base de datos."
        }
    }
)
async def create_new_alimentador(
    alimentador: Alimentador,
    db: MySQLConnection = Depends(get_db)
) -> Any:
    """Inserta una nueva autoridad alimentadora en la base de datos y retorna el registro creado.

    Args:
        alimentador (Alimentador): Modelo Pydantic con la información de la autoridad a registrar.
        db (MySQLConnection): Conexión activa a la base de datos inyectada por dependencia.

    Returns:
        Any: El modelo Alimentador persistido.

    Raises:
        HTTPException: Con código 400 (BAD REQUEST) si la inserción fue rechazada o ya existe un registro duplicado.
    """
    new_alimentador = await insert_new_alimentador(db, alimentador)

    if not new_alimentador:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error inserting alimentador. Verify whether the alimentador has not been registered already"
        )

    return new_alimentador

# GET ALIMENTADOR POR MUNICIPIO
# @router.get(
#     "/municipio/{municipio}",
#     response_model=list[Alimentador],
#     summary="Obtener alimentador por municipio",
#     description="Consulta los detalles y jurisdicción municipal de todos los alimentadores mediante su municipio.",
#     responses={
#         status.HTTP_200_OK: {
#             "model": list[Alimentador],
#             "description": "Alimentadores localizados exitosamente."
#         },
#         status.HTTP_404_NOT_FOUND: {
#             "description": "No existen alimentadores registrados con el municipio proporcionado."
#         },
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {
#             "description": "Error interno al consultar la base de datos."
#         }
#     }
# )
# async def read_alimentador_by_municipio(
#     municipio: str,
#     db: MySQLConnection = Depends(get_db)
# ) -> Any:
#     alimentadores = await get_all_alimentadores_by_municipio(db, municipio)

#     if not alimentadores:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Alimentadores with municipio {municipio} not found"
#         )

#     return alimentadores


@router.get(
    "/municipio/{municipio}",
    response_model=list[Alimentador],
    summary="Listar todos los alimentadores por municipio",
    description="Recupera el listado completo de todas las autoridades y alimentadores registrados en el sistema por municipio.",
    responses={
        status.HTTP_200_OK: {
            "model": list[Alimentador],
            "description": "Listado de autoridades alimentadoras obtenido exitosamente."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno de servidor o falla en la consulta de registros."
        }
    }
)
async def read_all_alimentadores_by_municipio(
    municipio: str, 
    db: MySQLConnection = Depends(get_db)
) -> Any:
    alimentadores = await get_all_alimentadores_by_municipio(db, municipio)
    return alimentadores