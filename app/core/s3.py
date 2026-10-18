"""Módulo de conexión y administración del s3 de AWS. 

Almacenar evidencias de Rieti en AWS
"""

import boto3
from app.core.config import settings 

def subir_foto (folio:str, num_foto:int, foto:bytes) -> dict:
    """Sube la evidencia a s3 y devuelve su url"""

    if num_foto < 1:
        raise ValueError("Número inválido")

    nombre = f"{folio}-{num_foto}.jpg"
    ruta = f"evidencias/{folio}/{nombre}"

    s3 = boto3.client("s3", region_name = "us-east-1")

    print ("Bucket:", settings.S3_BUCKET_NAME, flush= True)
    s3.put_object(
        Bucket = settings.S3_BUCKET_NAME,
        Key =ruta, 
        Body = foto, 
        ContentType = "image/jpeg",
        IfNoneMatch = "*"
    )

    return ruta

