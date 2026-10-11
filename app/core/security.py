"""Módulo de seguridad y validación de tokens de identidad JWT mediante AWS Cognito.

Verifica la firma criptográfica con llaves públicas JWKS y extrae la identidad del usuario (sub).
"""

import requests
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.config import settings

ISSUER = f"https://cognito-idp.{settings.AWS_COGNITO_REGION}.amazonaws.com/{settings.COGNITO_USER_POOL_ID}"
JWKS_URL = f"{ISSUER}/.well-known/jwks.json"

jwks = requests.get(JWKS_URL).json()
security = HTTPBearer()

def get_current_user_sub(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """Extrae y valida el identificador único de usuario (`sub`) desde el token Bearer JWT de AWS Cognito.

    Obtiene la cabecera del token JWT sin verificar, busca la clave pública correspondiente
    en el conjunto JWKS descargado de Cognito, decodifica y valida la firma criptográfica (algoritmo RS256),
    verificando la audiencia esperada (Client ID de Android) y el emisor (Issuer).

    Args:
        credentials (HTTPAuthorizationCredentials): Credenciales de autorización HTTP Bearer
            proporcionadas en el encabezado `Authorization`.

    Returns:
        str: El identificador único de sujeto (`sub`) del usuario autenticado en Cognito.

    Raises:
        HTTPException: Con código 401 (UNAUTHORIZED) si no se localiza la clave pública RSA asociada al `kid`
            del token, o si la validación criptográfica del JWT (expiración, firma, audiencia) falla.
    """
    token = credentials.credentials
    try:
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}

        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "user": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
                break

        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Public key not found. Token is invalid"
            )

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=settings.ANDROID_APP_CLIENT_ID,
            issuer=ISSUER
        )

        return payload["sub"]
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {str(e)}"
        )