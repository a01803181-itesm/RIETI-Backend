from pydantic import BaseModel, EmailStr

class Admin(BaseModel):
    correoAd: EmailStr
    contrasenia: str
    nombre: str
    ap_paterno: str
    ap_materno: str
    telefono: str