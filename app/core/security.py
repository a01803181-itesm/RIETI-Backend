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

DASHBOARD_ISSUER = f"https://cognito-idp.{settings.AWS_COGNITO_REGION}.amazonaws.com/" f"{settings.DASHBOARD_COGNITO_USER_POOL_ID}"
DASHBOARD_JWKS_URL = f"{DASHBOARD_ISSUER}/.well-known/jwks.json"

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

def get_dashboard_user (credentials:HTTPAuthorizationCredentials = Security(security)) -> dict:
        """Extrae y valida la identidad de un usuario autenticado en el Cognito del dashboard.

    Obtiene la cabecera del access token JWT, identifica la llave pública
    correspondiente en el conjunto JWKS de Cognito y verifica la firma
    criptográfica mediante RS256, el emisor y la expiración.

    Además, comprueba que el token sea de tipo access y que su Client ID
    corresponda a la aplicación web del dashboard.

    Args:
        credentials (HTTPAuthorizationCredentials): Credenciales de
            autenticación recibidas mediante el encabezado Authorization Bearer.

    Returns:
        dict: Claims verificadas del token JWT, incluyendo el identificador
            único del usuario (sub).

    Raises:
        HTTPException: Error 401 (UNAUTHORIZED) si el token es inválido,
            ha expirado, no corresponde al cliente esperado o no puede
            verificarse su firma criptográfica.
    """

        token = credentials.credentials

        error_credenciales = HTTPException(
             status_code= status.HTTP_401_UNAUTHORIZED,
             detail="Token invalido",
             headers ={"WWW-Authenticate": "Bearer"}
        )

        try:
             respuesta = requests.get(DASHBOARD_JWKS_URL, timeout=5)
             respuesta.raise_for_status()
             dashboard_jwks = respuesta.json()

             encabezado = jwt.get_unverified_header(token)

             if encabezado.get("alg")!="RS256":
                  raise error_credenciales

             llave = next(
             (
                  key for key in dashboard_jwks.get("keys", [])
                  if key.get("kid") == encabezado.get("kid")
                  and key.get("kty") =="RSA"
                  and key.get("use") == "sig"
             ),
             None
             )

             if llave is None:
                  raise error_credenciales

             payload =jwt.decode(
                  token,
                  llave,
                  algorithms= ["RS256"],
                  issuer= DASHBOARD_ISSUER,
                  options={"verify_aud": False}
             )

             if payload.get("token_use") != "access":
                  raise error_credenciales

             if payload.get("client_id") != settings.DASHBOARD_COGNITO_CLIENT_ID:
                  raise error_credenciales

             if not isinstance(payload.get("sub"), str) or not payload["sub"]:
                  raise error_credenciales

             return payload

        except HTTPException:
            raise

        except(JWTError, requests.RequestException, ValueError, KeyError):
             raise error_credenciales