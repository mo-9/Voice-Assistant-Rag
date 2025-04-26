import time
import functools
from app.logger import logger

def timed(task_name: str):
    def decorator(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = await fn(*args, **kwargs)
                elapsed = (time.time() - start) * 1000
                logger.info(f"{task_name} done in {elapsed:.0f} ms")
                return result
            except Exception as e:
                elapsed = (time.time() - start) * 1000
                logger.error(f"{task_name} failed in {elapsed:.0f} ms: {e}")
                raise
        return wrapper
    return decorator