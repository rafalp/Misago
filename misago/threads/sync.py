from asyncio import gather
from typing import Optional, Tuple

from ..database.objectmapper import ObjectMapperQuery
from .models import Post, Thread


async def get_thread_stats(
    thread_id: int, base_query: Optional[ObjectMapperQuery] = None
) -> dict:
    posts_query = (base_query or Post.query).filter(thread_id=thread_id)
    posts_count, last_post = await gather(
        posts_query.count(),
        posts_query.order_by("-id").limit(1).one(),
    )

    return {
        "replies": max(posts_count - 1, 0),
        "last_post": last_post,
    }


async def sync_thread(
    thread: Thread, base_query: Optional[ObjectMapperQuery] = None
) -> Tuple[Thread, dict]:
    stats = await get_thread_stats(thread.id, base_query)
    return (await thread.update(**stats)), stats


async def sync_thread_by_id(
    thread_id: int, base_query: Optional[ObjectMapperQuery] = None
) -> dict:
    stats = await get_thread_stats(thread_id, base_query)
    await Thread.query.filter(id=thread_id).update(
        replies=stats["replies"], last_post_id=stats["last_post"].id
    )
    return stats
