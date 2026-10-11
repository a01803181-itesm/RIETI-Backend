"""Endpoint de verificación de estado y salud del servicio."""

from fastapi import APIRouter, status

router = APIRouter()

@router.get(
    "",
    summary="Verificar estado del servicio",
    description="Endpoint de comprobación de salud (health check) que confirma la disponibilidad y operatividad básica de la API.",
    responses={
        status.HTTP_200_OK: {
            "description": "El servicio se encuentra activo y respondiendo peticiones.",
            "content": {
                "application/json": {
                    "example": {"status": "ok"}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Fallo crítico en el servidor o componentes internos."
        }
    }
)
def check() -> dict[str, str]:
    """Comprueba el estado y disponibilidad operativa de la API de RIETI.

    Args:
        None.

    Returns:
        dict[str, str]: Diccionario con la clave 'status' y valor 'ok'.

    Raises:
        None.
    """
    return { "status": "ok" }