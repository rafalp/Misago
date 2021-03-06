from typing import Optional

from ..cache import cache

FORUM_STATS_CACHE = "forum_stats"

CACHE_TIMEOUT = 60 * 60  # 1 hour


async def get_forum_stats_cache() -> Optional[dict]:
    return await cache.get(FORUM_STATS_CACHE)


async def set_forum_stats_cache(stats: dict):
    await cache.set(FORUM_STATS_CACHE, stats, ttl=CACHE_TIMEOUT)


async def clear_forum_stats_cache():
    await cache.delete(FORUM_STATS_CACHE)
