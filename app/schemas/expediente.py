"""Esquema Pydantic para el modelo de Expediente administrativo en RIETI."""

from pydantic import BaseModel, EmailStr, Field
from app.schemas.enums import Status

class Expediente(BaseModel):
    """Modelo de datos representativo de un expediente de investigación o canalización.

    Attributes:
        folioE (str): Folio alfanumérico identificador del expediente.
        lugar (str): Sede, dependencia física o juzgado donde radica el expediente.
        descripcion (str): Resumen del caso, diligencias realizadas y estatus de canalización.
        status (Status): Estado administrativo actual dentro del ciclo de vida del caso.
        correoAl (EmailStr): Correo de la autoridad o alimentador responsable asignado.
    """
    folioE: str = Field(
        ...,
        description="Identificador alfanumérico único del expediente administrativo.",
        examples=["EXP-2026-TOL-042"]
    )
    lugar: str = Field(
        ...,
        description="Dependencia, delegación o municipio donde se procesa el caso.",
        examples=["DIF Municipal Toluca - Procuraduría de Protección"]
    )
    descripcion: str = Field(
        ...,
        description="Descripción detallada de la intervención y medidas de protección implementadas.",
        examples=["Expediente iniciado tras confirmación de avistamiento; visita domiciliaria programada."]
    )
    status: Status = Field(
        ...,
        description="Estado administrativo actual dentro del flujo de atención del expediente."
    )
    correoAl: EmailStr = Field(
        ...,
        description="Correo institucional de la autoridad o alimentador asignado.",
        examples=["alimentador.toluca@rieti.org"]
    )