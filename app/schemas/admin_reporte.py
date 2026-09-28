from pydantic import BaseModel, EmailStr

class AdminReporte(BaseModel):
    correoAd: EmailStr
    folio: str