from pydantic import BaseModel, EmailStr
from app.schemas.enums import Provider

class Alimentador(BaseModel):
    correoAl: EmailStr
    contrasenia: str
    proveedor: Provider
    telefono: str
    nombre: str
    ap_paterno: str
    ap_materno: str
    municipio: str

class PublicAlimentador(BaseModel):
    correoAl: EmailStr
    proveedor: str
    telefono: str
    nombre: str
    ap_paterno: str
    ap_materno: str
    municipio: str