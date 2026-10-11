"""Esquema Pydantic para el modelo de Evidencias multimedia de reportes en RIETI."""

from pydantic import BaseModel, Field

class Evidencia(BaseModel):
    """Modelo de datos representativo de archivos multimedia o pruebas adjuntas a un reporte.

    Attributes:
        id (int): Identificador autonumérico del registro en base de datos.
        url (str): Localizador uniforme de recursos (URL o URI en S3) del archivo multimedia.
        folio (str): Folio del reporte al que pertenece la evidencia fotográfica o documental.
    """
    id: int = Field(
        ...,
        description="Identificador único del registro de evidencia en base de datos.",
        examples=[101]
    )
    url: str = Field(
        ...,
        description="URL accesible o ruta de almacenamiento del archivo de evidencia.",
        examples=["https://s3.amazonaws.com/rieti-evidencias/REP-2026-001/foto1.jpg"]
    )
    folio: str = Field(
        ...,
        description="Folio del reporte al que se asocia la evidencia.",
        examples=["REP-2026-001"]
    )