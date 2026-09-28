from pydantic import BaseModel, AwareDatetime, EmailStr
from pydantic_extra_types.coordinate import Latitude, Longitude

class Reporte(BaseModel):
    folio: str
    edad: int
    dia: AwareDatetime
    tipoTrabajo: str
    numNNA: int
    direccion: str
    latitud: Latitude
    longitud: Longitude
    nombre: str
    ap_materno: str
    ap_paterno: str
    correoU: EmailStr
    folioE: str
    correoAl: EmailStr