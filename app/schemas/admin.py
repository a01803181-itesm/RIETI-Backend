from pydantic import BaseModel, EmailStr
from app.schemas.enums import Provider

class Admin(BaseModel):
    correoAd: EmailStr
    proveedor: Provider
    nombre: str
    ap_paterno: str
    ap_materno: str
    telefono: str