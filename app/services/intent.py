from app.utils.metrics import timed

@timed("Intent Classification")
async def classify_intent(text: str) -> str:
    return "sql_query" if text.lower().startswith("sql:") else "chat"