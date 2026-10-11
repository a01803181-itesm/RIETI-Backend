"""Esquema Pydantic para la relación y bitácora entre administradores y reportes."""

from pydantic import BaseModel, EmailStr, Field

class AdminReporte(BaseModel):
    """Modelo asociativo que registra las actuaciones o notas de un Administrador sobre un Reporte.

    Attributes:
        correoAd (EmailStr): Correo electrónico del administrador que gestiona el reporte.
        folio (str): Identificador único del reporte asociado.
        descripcion (str): Nota descriptiva o bitácora de la gestión realizada.
    """
    correoAd: EmailStr = Field(
        ...,
        description="Correo electrónico del administrador que gestiona el reporte.",
        examples=["admin.central@rieti.org"]
    )
    folio: str = Field(
        ...,
        description="Identificador alfanumérico único del reporte asociado.",
        examples=["REP-2026-001"]
    )
    descripcion: str = Field(
        ...,
        description="Bitácora, notas de intervención o comentarios de seguimiento.",
        examples=["Se canalizó el caso con DIF municipal para visita domiciliaria."]
    )