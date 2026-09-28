from pydantic import BaseModel, EmailStr

class Usuario(BaseModel):
    correoU: EmailStr
    contrasenia: str

class PublicUsuario(BaseModel):
    correoU: EmailStr
