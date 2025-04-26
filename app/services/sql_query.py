import asyncpg
from app.config import settings
from app.utils.metrics import timed

@timed("SQL Query")
async def execute_query(query: str, dsn: str = None) -> list[dict]:
    conn = await asyncpg.connect(dsn or settings.postgres_diy_dsn)
    try:
        rows = await conn.fetch(query)
        return [dict(r) for r in rows]
    finally:
        await conn.close()
