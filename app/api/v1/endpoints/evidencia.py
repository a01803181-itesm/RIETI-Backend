"""Endpoints de evidencias/fotografias """

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from asyncmy import Connection as MySQLConnection 
from app.core.db_connection import get_db
from app.core.s3 import subir_foto, obtener_url_de_foto
from app.crud.reporte import get_reporte_by_folio
from app.crud.evidencia import insert_new_evidencia, get_evidencia, get_num_foto, get_evidencias_by_folio

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

    num_foto = await get_num_foto (db, folio)

    try: 

        ruta = subir_foto(folio, num_foto, contenido)

        evidencia_id = await insert_new_evidencia(db, folio, ruta)

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

@router.get ("/by-folio/{folio}")
async def obtener_evidencias_de_folio ( folio: str, db:MySQLConnection = Depends(get_db)):
    """Obtener las fotos de un reporte"""
    reporte = await get_reporte_by_folio(db, folio)

    if not reporte:
        raise HTTPException(
            status_code= 404, 
            detail= "No se encontro reporte"
        )

    evidencias = await get_evidencias_by_folio(db, folio)

    return [
        {
            "id": evidencias[0],
            "url": obtener_url_de_evidencia(evidencias[1]),
            "folio": evidencias[2]
        }

        for evidencia in evidencias
    ]

@router.get("/{id}/url")

async def obtener_url_de_evidencia( id:int, db: MySQLConnection = Depends (get_db)): 
    evidencia = await get_evidencia (db, id)

    if not evidencia:
        raise HTTPException(
            status_code= 404, 
            detail= "No se encontro la evidencia"
        )

    ruta = evidencia[1]

    url = obtener_url_de_foto(ruta)

    return {
        "id": id,
        "url": url,
        "expira en": 300
    }