import asyncpg
from app.config import settings
from app.logger import logger
from app.utils.metrics import timed

@timed("Vector Search")
async def vector_search(query: str, top_k: int = 5) -> list[dict]:
    if not settings.use_vector_search:
        logger.info("Vector search disabled, skipping.")
        return []

    conn = None
    try:
        conn = await asyncpg.connect(settings.postgres_dsn)
        # fallback to simple ILIKE on your real table/column
        table  = settings.search_table
        column = settings.search_column
        sql = f"""
          SELECT *
          FROM {table}
          WHERE {column} ILIKE '%' || $1 || '%'
          LIMIT $2
        """
        records = await conn.fetch(sql, query, top_k)
        return [dict(r) for r in records]

    except Exception as e:
        logger.warning(f"Vector search failed ({e}), returning no hits.")
        return []

    finally:
        if conn:
            await conn.close()
