from pydantic import BaseModel

class Evidencia(BaseModel):
    id: int
    url: str
    folio: str