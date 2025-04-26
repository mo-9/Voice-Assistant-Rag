from aiocache import cached, Cache
from app.config import settings

@cached(ttl=settings.cache_ttl_seconds, cache=Cache.MEMORY)
async def cached_search(key: str, fn, *args, **kwargs):
    return await fn(*args, **kwargs)