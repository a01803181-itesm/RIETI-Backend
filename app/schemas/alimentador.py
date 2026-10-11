"""Esquema Pydantic para el modelo de Alimentador (Autoridad de campo) en RIETI."""

from pydantic import BaseModel, EmailStr, Field
from app.schemas.enums import Provider

class Alimentador(BaseModel):
    """Modelo de datos representativo de una autoridad o usuario alimentador de campo.

    Attributes:
        correoAl (EmailStr): Correo institucional de la autoridad o alimentador.
        proveedor (Provider): Proveedor de autenticación utilizado (Cognito o Google).
        telefono (str): Número telefónico de contacto institucional.
        nombre (str): Nombre(s) de la autoridad o funcionario.
        ap_paterno (str): Primer apellido del funcionario.
        ap_materno (str): Segundo apellido del funcionario.
        municipio (str): Municipio o demarcación territorial asignada.
    """
    correoAl: EmailStr = Field(
        ...,
        description="Correo institucional de la autoridad o alimentador de campo.",
        examples=["alimentador.toluca@rieti.org"]
    )
    proveedor: Provider = Field(
        ...,
        description="Proveedor de identidad federada empleado para autenticación."
    )
    telefono: str = Field(
        ...,
        description="Número de teléfono de contacto institucional a 10 dígitos.",
        examples=["7221234567"]
    )
    nombre: str = Field(
        ...,
        description="Nombre(s) de pila de la autoridad o funcionario.",
        examples=["Carlos"]
    )
    ap_paterno: str = Field(
        ...,
        description="Primer apellido de la autoridad o funcionario.",
        examples=["Ramírez"]
    )
    ap_materno: str = Field(
        ...,
        description="Segundo apellido de la autoridad o funcionario.",
        examples=["Pérez"]
    )
    municipio: str = Field(
        ...,
        description="Municipio o jurisdicción territorial asignada para atención.",
        examples=["Atizapán"]
    )