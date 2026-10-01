from pydantic import BaseModel, EmailStr
from app.schemas.enums import Status

class Expediente(BaseModel):
    folioE: str
    lugar: str
    descripcion: str
    estatus: Status
    correoAl: EmailStr