from typing import List, Optional, Sequence

from ..database import database
from ..tables import posts, threads
from ..types import Post, Thread


async def get_post_by_id(post_id: int) -> Optional[Post]:
    query = posts.select().where(posts.c.id == post_id)
    data = await database.fetch_one(query)
    return Post(**data) if data else None


async def get_posts_by_id(ids: Sequence[int]) -> List[Post]:
    query = posts.select().where(posts.c.id.in_(ids))
    data = await database.fetch_all(query)
    return [Post(**row) for row in data]


async def get_thread_by_id(thread_id: int) -> Optional[Thread]:
    query = threads.select().where(threads.c.id == thread_id)
    data = await database.fetch_one(query)
    return Thread(**data) if data else None


async def get_threads_by_id(ids: Sequence[int]) -> List[Thread]:
    query = threads.select().where(threads.c.id.in_(ids))
    data = await database.fetch_all(query)
    return [Thread(**row) for row in data]
