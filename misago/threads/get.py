from typing import Awaitable, List, Sequence

from ..database.paginator import Paginator
from .models import Post, Thread


def get_posts_by_id(ids: Sequence[int]) -> Awaitable[List[Post]]:
    return Post.query.filter(id__in=ids).all()


def get_threads_by_id(ids: Sequence[int]) -> Awaitable[List[Thread]]:
    return Thread.query.filter(id__in=ids).all()


async def get_thread_posts_paginator(
    thread: Thread, per_page: int, orphans: int = 0
) -> Paginator:
    paginator = Paginator(
        thread.posts_query.order_by("id"),
        per_page,
        orphans,
        overlap_pages=True,
    )
    await paginator.count_pages()
    return paginator
