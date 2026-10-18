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
