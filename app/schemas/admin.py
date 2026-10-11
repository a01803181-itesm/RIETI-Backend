"""Esquema Pydantic para el modelo de Administrador del sistema RIETI."""

from pydantic import BaseModel, EmailStr, Field
from app.schemas.enums import Provider

class Admin(BaseModel):
    """Modelo de datos que representa a un usuario con rol de Administrador.

    Attributes:
        correoAd (EmailStr): Correo electrónico institucional único del administrador.
        proveedor (Provider): Proveedor de identidad federada (Cognito o Google).
        nombre (str): Nombre(s) de pila del administrador.
        ap_paterno (str): Primer apellido del administrador.
        ap_materno (str): Segundo apellido del administrador.
        telefono (str): Número telefónico de contacto directo.
    """
    correoAd: EmailStr = Field(
        ...,
        description="Correo electrónico institucional único del administrador.",
        examples=["admin.central@rieti.org"]
    )
    proveedor: Provider = Field(
        ...,
        description="Proveedor de identidad federada empleado para autenticación."
    )
    nombre: str = Field(
        ...,
        description="Nombre(s) de pila del administrador.",
        examples=["Laura"]
    )
    ap_paterno: str = Field(
        ...,
        description="Primer apellido del administrador.",
        examples=["Gómez"]
    )
    ap_materno: str = Field(
        ...,
        description="Segundo apellido del administrador.",
        examples=["Hernández"]
    )
    telefono: str = Field(
        ...,
        description="Número telefónico de contacto directo a 10 dígitos.",
        examples=["5512345678"]
    )