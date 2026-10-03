from pydantic import BaseModel, EmailStr
from app.schemas.enums import Provider

class Usuario(BaseModel):
    correoU: EmailStr
    proveedor: Provider

class CheckEmail(BaseModel):
    exists: bool
    provider: Provider | None
