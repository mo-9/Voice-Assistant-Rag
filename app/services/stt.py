import io
from openai import AsyncOpenAI
from app.utils.metrics import timed

client = AsyncOpenAI(api_key="")
@timed("STT")
async def transcribe(audio_bytes: bytes) -> str:

    buffer = io.BytesIO(audio_bytes)
    buffer.name = "audio.wav"

    resp = await client.audio.transcriptions.create(
        file=buffer,
        model="whisper-1",
        response_format="text"
    )

    return resp.strip()
