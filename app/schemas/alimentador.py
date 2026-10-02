from pydantic import BaseModel, EmailStr
from app.schemas.enums import Provider

class Alimentador(BaseModel):
    correoAl: EmailStr
    proveedor: Provider
    telefono: str
    nombre: str
    ap_paterno: str
    ap_materno: str
    municipio: str