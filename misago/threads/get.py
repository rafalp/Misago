from typing import Awaitable, List, Optional, Sequence

from ..categories.models import Category
from ..database.paginator import PageDoesNotExist, Paginator
from .models import Post, Thread, ThreadPostsPage, ThreadsFeed


def get_posts_by_id(ids: Sequence[int]) -> Awaitable[List[Post]]:
    return Post.query.filter(id__in=ids).all()


def get_threads_by_id(ids: Sequence[int]) -> Awaitable[List[Thread]]:
    return Thread.query.filter(id__in=ids).all()


async def get_thread_posts_paginator(
    thread: Thread, per_page: int, orphans: int = 0
) -> Paginator:
    paginator = Paginator(
        thread.posts_query.order_by("id"), per_page, orphans, overlap_pages=True
    )
    await paginator.count_pages()
    return paginator


async def get_thread_posts_page(
    paginator: Paginator, page: int
) -> Optional[ThreadPostsPage]:
    try:
        posts_page = await paginator.get_page(page)
    except PageDoesNotExist:
        return None
    return ThreadPostsPage.from_paginator_page(posts_page, await posts_page.items)


async def get_threads_feed(
    threads_per_page: int,
    cursor: Optional[int] = None,
    *,
    categories: Optional[Sequence[Category]] = None,
    starter_id: Optional[int] = None,
) -> ThreadsFeed:
    if categories is not None and not categories:
        return ThreadsFeed()

    query = Thread.query.order_by("-last_post_id").limit(threads_per_page + 1)
    if categories:
        query = query.filter(category_id__in=[category.id for category in categories])
    if starter_id:
        query = query.filter(starter_id=starter_id)
    if cursor:
        query = query.filter(last_post_id__lt=cursor)

    results = await query.all()
    if len(results) > threads_per_page:
        results = results[:-1]
        next_cursor = results[-1].last_post_id
    else:
        next_cursor = None

    return ThreadsFeed(items=results, next_cursor=next_cursor)
