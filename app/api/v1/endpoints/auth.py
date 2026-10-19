"""Endpoints de autenticación admin o alimentador del dashboard de RIETI."""

import requests

from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from asyncmy import Connection as MySQLConnection

from app.core.config import settings
from app.core.db_connection import get_db
from app.core.security import get_dashboard_user
from app.crud.admin import get_admin
from app.crud.alimentador import get_alimentador
from app.schemas.enums import Provider


router = APIRouter()

@router.get("/identity", summary="Consultar indetidad y rol ", description="valida el access token del dashoard con cognito y consulta el rol con sql" )

async def get_identity(usuario: dict = Depends(get_dashboard_user), credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()), db: MySQLConnection = Depends(get_db)):
    """Devuelve el identificador del usuario y rol"""

    url = "https://us-east-16krvaj19v.auth.us-east-1.amazoncognito.com/oauth2/userInfo"

    try:
        respuesta =requests.get( 
            url, 
            headers= {"Authorization":f"Bearer {credentials.credentials}" },
            timeout= 5
        )

        respuesta.raise_for_status()
        datos = respuesta.json()

    except (requests.RequestException, ValueError):
        raise HTTPException(
            status_code= status.HTTP_502_BAD_GATEWAY,
            detail="No se pudo consultar identidad en cognito"
        )

    if datos.get("sub") != usuario ["sub"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "La identidad no coicide"
        )

    if datos.get ("email_verified") not in (True, "true"):
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Correo no verificado"
        )

    correo = datos.get("email")

    if not isinstance(correo, str) or not correo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "No correo"
        )

    admin = await get_admin(db,correo)
    alimentador = await get_alimentador(db, correo)

    proveedor = obtener_proveedor(usuario)

    es_Admin= (admin is not None and admin.proveedor == proveedor)

    es_Alimentador =( alimentador is not None  and alimentador.proveedor == proveedor)

    if es_Admin:
        rol = "admin"

    elif es_Alimentador:
        rol = "alimentador"

    else: 
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Usuario sin autorización"
        )

    return {
        "sub": usuario["sub"],
        "correo": correo,
        "rol": rol
    }

def obtener_proveedor (usuario:dict) -> Provider:
    username = usuario.get("username")

    if isinstance(username, str) and username.startswith("Google_"):
        return Provider.GOOGLE

    return Provider.COGNITO