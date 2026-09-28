from pydantic import BaseModel, EmailStr

class Alimentador(BaseModel):
    correoAl: EmailStr
    contrasenia: str
    telefono: str
    nombre: str
    ap_paterno: str
    ap_materno: str
    municipio: str