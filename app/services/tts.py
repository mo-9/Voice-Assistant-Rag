from openai import OpenAI,AsyncOpenAI
from app.config import settings
from app.utils.metrics import timed

client_tts =  AsyncOpenAI(api_key="")
@timed("TTS")
async def synthesize(text: str) -> bytes:
    # Read binary TTS output directly
    resp = await client_tts.audio.speech.create(
        model="tts-1",  # specify the TTS model
        input=text,
        voice="alloy"
    )
    # resp is HttpxBinaryResponseContent; await it to get raw bytes
    data = await resp.aread()
    return data