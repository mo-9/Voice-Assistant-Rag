from openai import OpenAI,AsyncOpenAI
from app.config import settings
from app.utils.metrics import timed

client_llm = AsyncOpenAI(api_key="")
@timed("LLM Refinement")
async def refine_answer(system_prompt: str, user_content: str) -> str:
    resp = await client_llm.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
    )
    return resp.choices[0].message.content