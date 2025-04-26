from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import asyncpg

from app.services import   stt, intent,vector_search, sql_query, llm,  tts,  db_retrieve

from app.logger import logger
from app.config import settings

app = FastAPI()

@app.post("/assist/stream")
async def assist_stream(audio: UploadFile):
    data = await audio.read()
    logger.info("t0: audio received")

    text = await stt.transcribe(data)
    intent_name = await intent.classify_intent(text)

    if intent_name == "sql_query":
        results = await sql_query.execute_query(text[len("sql:"):])
        answer = str(results)
    else:
        vect_hits = await vector_search.vector_search(text)
        sources = "\n".join(h["content"] for h in vect_hits)
        prompt = f"User: {text}\nSources:\n{sources}"
        answer = await llm.refine_answer("You are a helpful assistant.", prompt)

    audio_bytes = await tts.synthesize(answer)
    return StreamingResponse(iter([audio_bytes]), media_type="audio/mpeg")


@app.get("/tables")
async def list_tables():
    conn = await asyncpg.connect(settings.postgres_dsn)
    rows = await conn.fetch("""
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public';
    """)
    await conn.close()
    return [r["table_name"] for r in rows]


@app.get("/query/")
async def run_query(sql: str):
    try:
        results = await sql_query.execute_query(sql)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/db/{table_name}")
async def get_table(table_name: str, limit: int = 10):
    try:
        data = await db_retrieve.retrieve_table(table_name, limit)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
