from pydantic import BaseModel, AwareDatetime, EmailStr
from pydantic_extra_types.coordinate import Latitude, Longitude
from app.schemas.enums import MunicipioEnum

class Reporte(BaseModel):
    folio: str
    edad: int | None = None
    dia: AwareDatetime
    tipoTrabajo: str
    numNinios: int | None = None
    direccion: str
    municipio: MunicipioEnum
    latitud: Latitude
    longitud: Longitude
    nombre: str
    ap_paterno: str
    ap_materno: str
    detalles_adcionales: str | None = None
    correoU: EmailStr | None = None
    folioE: str | None = None
    correoAl: EmailStr | None = None

