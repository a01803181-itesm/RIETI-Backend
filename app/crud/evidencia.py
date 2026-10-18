"""Módulo de operaciones CRUD para la entidad de Evidencia en MySQL."""

from asyncmy import Connection as MySQLConnection 

async def insert_new_evidencia(conn: MySQLConnection, folio:str, ruta:str ) -> int:
    """Guarda la ruta de una fotografia de un reporte"""

    query = """
        INSERT INTO Evidencia (url, folio)
        VALUES (%s, %s);
    """

    async with conn.cursor() as cur:
        await cur.execute (query, (ruta, folio))
        await conn.commit()

        return cur.lastrowid


async def get_evidencia (conn:MySQLConnection, id: int):
    query = """
        SELECT id, url, folio
        FROM Evidencia
        WHERE id = %s
    """

    async with conn.cursor() as cur:
        await cur.execute(query, (id,))
        return await cur.fetchone()



async def get_num_foto (conn:MySQLConnection, folio:str) -> int:
    query = """
    SELECT url 
    FROM Evidencia
    WHERE folio = %s
    """
    async with conn.cursor () as cur:
        await cur.execute (query, (folio,))
        evidencias = await cur.fetchall()

    nums = []

    for evidencia in evidencias:
        ruta = evidencia[0]
        nombre = ruta.rsplit("/", 1)[-1]

        try:
            num = int (nombre.rsplit("-", 1)[-1].replace (".jpg", ""))
            nums.append(num)
        
        except ValueError:
            continue

    return max(nums, default=0) + 1

async def get_evidencias_by_folio ( conn: MySQLConnection, folio:str):
    """Obteniendo todas las evidencias de un solo reporte"""

    query = """
    SELECT id, url, folio
    FROM Evidencia 
    WHERE folio = %s
    ORDER BY id ASC
    """

    async with conn.cursor() as cur:
        await cur.execute(query, (folio,))
        evidencias = await cur.fetchall()

    return evidencias 