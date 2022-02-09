from asyncio import gather
from dataclasses import dataclass
from typing import Awaitable, List, Optional, Sequence, Iterable, Union

from ..database.objectmapper import ObjectMapper, ObjectMapperQuery
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


@dataclass
class ThreadsPage:
    results: List[Thread]
    has_next: bool
    has_previous: bool
    next: Optional[int]
    previous: Optional[int]


async def get_threads_page(
    length: int,
    *,
    categories_ids: Optional[Iterable[int]] = None,
    starter_id: Optional[int] = None,
    after: Optional[int] = None,
    before: Optional[int] = None,
) -> ThreadsPage:
    if not categories_ids:
        return ThreadsPage(
            results=[],
            has_next=False,
            has_previous=False,
            next=None,
            previous=None,
        )

    query = Thread.query
    if categories_ids:
        query = query.filter(category_id__in=categories_ids)
    if starter_id:
        query = query.filter(starter_id=starter_id)

    if after and before:
        raise ValueError("'after' and 'before' kwargs are exclusive")

    if before:
        return await slice_threads_using_before(query, length, before)

    return await slice_threads_using_after(query, length, after)


async def slice_threads_using_after(
    base_query: Union[ObjectMapper, ObjectMapperQuery],
    length: int,
    cursor: Optional[int],
):
    if cursor:
        results_query = base_query.filter(last_post_id__lt=cursor)
    else:
        results_query = base_query

    results_query = results_query.order_by("-last_post_id").limit(length + 1).all()

    if cursor:
        previous_query = (
            base_query.filter(last_post_id__gte=cursor)
            .order_by("last_post_id")
            .limit(1)
            .one("last_post_id")
        )
        results, previous = await gather(results_query, previous_query)
        previous = previous["last_post_id"]
    else:
        results = await results_query
        previous = None

    if len(results) > length:
        next = results[-1].last_post_id
        results = results[:-1]
    else:
        next = None

    return ThreadsPage(
        results=results,
        has_next=bool(next),
        has_previous=bool(previous),
        next=next,
        previous=previous,
    )


async def slice_threads_using_before(
    base_query: Union[ObjectMapper, ObjectMapperQuery],
    length: int,
    cursor: int,
):
    results_query = (
        base_query.filter(last_post_id__gt=cursor)
        .order_by("last_post_id")
        .limit(length + 1)
        .all()
    )

    if cursor:
        next_query = (
            base_query.filter(last_post_id__lte=cursor)
            .order_by("-last_post_id")
            .limit(1)
            .one("last_post_id")
        )
        results, next = await gather(results_query, next_query)
        next = next["last_post_id"]
    else:
        results = await results_query
        next = None

    if len(results) > length:
        previous = results[-1].last_post_id
        results = results[:-1]
    else:
        previous = None

    return ThreadsPage(
        results=list(reversed(results)),
        has_next=bool(next),
        has_previous=bool(previous),
        next=next,
        previous=previous,
    )
