from pydantic import BaseModel, EmailStr
from app.schemas.enums import Provider

class Usuario(BaseModel):
    correoU: EmailStr
    contrasenia: str | None = None
    proveedor: Provider

class PublicUsuario(BaseModel):
    correoU: EmailStr
    proveedor: str
