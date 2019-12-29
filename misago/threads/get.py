from typing import List, Optional, Sequence

from sqlalchemy import desc

from ..database import database
from ..database.paginator import PageDoesNotExist, Paginator
from ..tables import posts, threads
from ..types import Category, Post, Thread, ThreadPostsPage, ThreadsFeed


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


async def get_thread_posts_page(
    thread: Thread, per_page: int, orphans: int, page: int
) -> Optional[ThreadPostsPage]:
    query = posts.select().where(posts.c.thread_id == thread.id)
    paginator = Paginator(query, per_page, orphans, overlap_pages=True)
    try:
        posts_page = await paginator.get_page(page)
    except PageDoesNotExist:
        return None
    data = await database.fetch_all(posts_page.query.order_by(desc(posts.c.id)))
    return ThreadPostsPage.from_paginator_page(
        posts_page, [Post(**row) for row in data]
    )


async def get_threads_feed(
    threads_per_page: int,
    cursor: Optional[int] = None,
    *,
    categories: Optional[Sequence[Category]] = None,
    starter_id: Optional[int] = None,
) -> ThreadsFeed:
    query = (
        threads.select(None)
        .order_by(desc(threads.c.last_post_id))
        .limit(threads_per_page + 1)
    )

    if categories is not None:
        if not categories:
            return ThreadsFeed()
        categories_ids = [i.id for i in categories]
        query = query.where(threads.c.category_id.in_(categories_ids))
    if starter_id:
        query = query.where(threads.c.starter_id == starter_id)
    if cursor:
        query = query.where(threads.c.last_post_id < cursor)

    rows = await database.fetch_all(query)
    if len(rows) > threads_per_page:
        rows = rows[:-1]
        next_cursor = rows[-1]["last_post_id"]
    else:
        next_cursor = None

    return ThreadsFeed(items=[Thread(**row) for row in rows], next_cursor=next_cursor)
