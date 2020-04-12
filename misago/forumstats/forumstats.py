from ..database.queries import count
from ..tables import posts, threads, users
from ..utils.strings import get_random_string
from .cache import get_forum_stats_cache, set_forum_stats_cache


async def get_forum_stats() -> dict:
    forum_stats = await get_forum_stats_cache()
    if forum_stats is None:
        forum_stats = await get_forum_stats_from_db()
        await set_forum_stats_cache(forum_stats)
    return forum_stats


async def get_forum_stats_from_db() -> dict:
    return {
        "id": get_random_string(),
        "threads": await count(threads),
        "posts": await count(posts),
        "users": await count(users),
    }
