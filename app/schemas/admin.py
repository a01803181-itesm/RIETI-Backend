from pydantic import BaseModel, EmailStr
from app.schemas.enums import Provider

class Admin(BaseModel):
    correoAd: EmailStr
    contrasenia: str | None = None
    proveedor: Provider
    nombre: str
    ap_paterno: str
    ap_materno: str
    telefono: str

class PublicAdmin(BaseModel):
    correoAd: EmailStr
    proveedor: str
    nombre: str
    ap_paterno: str
    ap_materno: str
    telefono: str