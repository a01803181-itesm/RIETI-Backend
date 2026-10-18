"""Endpoints de evidencias/fotografias """

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from asyncmy import Connection as MySQLConnection 
from app.core.db_connection import get_db
from app.core.s3 import subir_foto
from app.crud.reporte import get_reporte_by_folio
from app.crud.evidencia import insert_new_evidencia

router = APIRouter()

@router.post ("/{folio}")

async def crear_evidencia( folio: str, foto:UploadFile = File (...), db: MySQLConnection = Depends(get_db)): 
    """Recibe una foto, la sube a s3 y la registra"""

    reporte = await get_reporte_by_folio(db, folio)

    if not reporte:
        raise HTTPException(
            status_code=404,
            detail= "Reporte no encontrado"
        )

    if foto.content_type != "image/jpeg":
        raise HTTPException(
            status_code= 400,
            detail= "No es JPEG"
        )

    contenido = await foto.read ( 5* 1024*1024 +1) #5 MB

    if len(contenido)> 5*1024*1024:
        raise HTTPException(
            status_code= 413,
            detail= "La foto supera 5MB"
        )

    num_foto = 1

    try: 
        print ("Incio de subir s3", flush= True)
        ruta = subir_foto(folio, num_foto, contenido)
        print ("foto subida en s3", ruta, flush= True)
        evidencia_id = await insert_new_evidencia(db, folio, ruta)
        print ("evidencia se guarda en swql", evidencia_id, flush= True)
    except Exception:
        raise HTTPException(
            status_code= 500, 
            detail= "No se pudo guardar la evidencia"
        ) 

    return {
        "id" : evidencia_id, 
        "folio": folio,
        "url": ruta 
    }