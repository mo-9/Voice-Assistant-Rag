import asyncpg
from app.config import settings
from app.utils.metrics import timed

@timed("DB Retrieve")
async def retrieve_table(table: str, limit: int = 10) -> list[dict]:
    conn = await asyncpg.connect(settings.postgres_diy_dsn)
    try:
        rows = await conn.fetch(f"SELECT * FROM {table} LIMIT {limit}")
        return [dict(r) for r in rows]
    finally:
        await conn.close()