"""Esquemas Pydantic para el modelo de Usuario ciudadano y comprobación de correo."""

from pydantic import BaseModel, EmailStr, Field
from app.schemas.enums import Provider

class Usuario(BaseModel):
    """Modelo de datos representativo de un usuario ciudadano registrado en la plataforma.

    Attributes:
        correoU (EmailStr): Correo electrónico del usuario ciudadano.
        proveedor (Provider): Proveedor de autenticación empleado (Cognito o Google).
    """
    correoU: EmailStr = Field(
        ...,
        description="Correo electrónico del usuario ciudadano registrado.",
        examples=["ciudadano.ejemplo@gmail.com"]
    )
    proveedor: Provider = Field(
        ...,
        description="Proveedor de identidad federada empleado para autenticación."
    )

class CheckEmail(BaseModel):
    """Respuesta a la verificación de existencia previa de una cuenta de usuario.

    Attributes:
        exists (bool): Indica si la dirección de correo ya se encuentra registrada en la base de datos.
        provider (Provider | None): Proveedor de identidad vinculado en caso de existir, o None.
    """
    exists: bool = Field(
        ...,
        description="Indica si la dirección de correo electrónico ya está registrada en el sistema.",
        examples=[True]
    )
    provider: Provider | None = Field(
        default=None,
        description="Proveedor de autenticación previamente asociado al correo si existe.",
        examples=[Provider.GOOGLE]
    )
