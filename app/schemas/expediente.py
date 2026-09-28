from enum import Enum
from pydantic import BaseModel, EmailStr

class Status(str, Enum):
    REGISTRADO = '1_Registrado'
    EN_REVISION = '2_En_revision'
    EN_SEGUIMIENTO = '3_En_seguimiento'
    CANALIZADO = '4_Canalizado'
    CONCLUIDO = '5_Concluido'
    ARCHIVADO = '6_Archivado'
    CANCELADO = '7_Cancelado'
    REINCIDENTE = '8_Reincidente'

class Expediente(BaseModel):
    folioE: str
    lugar: str
    descripcion: str
    status: Status
    correoAl: EmailStr