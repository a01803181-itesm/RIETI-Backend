from pydantic import BaseModel, AwareDatetime, EmailStr
from pydantic_extra_types.coordinate import Latitude, Longitude
from app.schemas.enums import RangoEdad, TipoTrabajo
from datetime import datetime
from typing import Any

class Reporte(BaseModel):
    folio: str
    edad: RangoEdad
    dia: datetime
    tipoTrabajo: TipoTrabajo
    numNinios: int | None = None
    direccion: str
    municipio: str
    latitud: Latitude
    longitud: Longitude
    nombre: str | None = None
    ap_paterno: str | None = None
    ap_materno: str | None = None
    detalles_adcionales: str | None = None
    correoU: EmailStr
    folioE: str | None = None
    correoAl: EmailStr | None = None

class CoordenadaReporte(BaseModel):
    lat: float
    lng: float

class CategoriaTotal(BaseModel):
    categoria: str
    total: int

# class MesTotal(BaseModel):
#     mes: str
#     total: int

class Data(BaseModel):
    data: float

class DataInt(BaseModel):
    data: int

class DashboardData(BaseModel):
    promedioResolucion: float
    pendientesUltimaSemana: int
    porcentajeEnProceso: float
    porcentajePendientes: float

class CantidadReportes(BaseModel):
    total: int
    completados: int
    en_proceso: int
    pendientes: int


