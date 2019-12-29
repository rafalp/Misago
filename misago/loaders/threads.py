from typing import Awaitable, Iterable, Optional, Sequence, Union

from ..types import Category, GraphQLContext, Thread, ThreadsFeed
from ..threads.get import get_threads_by_id, get_threads_feed
from .loader import get_loader, positive_int


def load_thread(
    context: GraphQLContext, thread_id: Union[int, str]
) -> Awaitable[Optional[Thread]]:
    loader = get_loader(context, "thread", get_threads_by_id)
    return loader.load(thread_id)


def load_threads(
    context: GraphQLContext, ids: Sequence[Union[int, str]]
) -> Awaitable[Sequence[Optional[Thread]]]:
    loader = get_loader(context, "thread", get_threads_by_id)
    return loader.load_many(ids)


async def load_threads_feed(
    context: GraphQLContext,
    *,
    cursor: Optional[Union[int, str]] = None,
    categories: Optional[Sequence[Category]] = None,
    starter_id: Optional[Union[int, str]] = None,
) -> Optional[ThreadsFeed]:
    if cursor:
        clean_cursor = positive_int(cursor)
        if not clean_cursor:
            return None
    else:
        clean_cursor = None

    if starter_id:
        clean_starter_id = positive_int(starter_id)
        if not clean_starter_id:
            return None
    else:
        clean_starter_id = None

    feed = await get_threads_feed(
        context["settings"]["threads_per_page"],
        clean_cursor,
        categories=categories,
        starter_id=clean_starter_id,
    )

    store_threads(context, feed.items)

    return feed


def store_thread(context: GraphQLContext, thread: Thread):
    loader = get_loader(context, "thread", get_threads_by_id)
    loader.clear(thread.id)
    loader.prime(thread.id, thread)


def store_threads(context: GraphQLContext, threads: Iterable[Thread]):
    loader = get_loader(context, "thread", get_threads_by_id)
    for thread in threads:
        loader.clear(thread.id)
        loader.prime(thread.id, thread)


def clear_thread(context: GraphQLContext, thread: Thread):
    loader = get_loader(context, "thread", get_threads_by_id)
    loader.clear(thread.id)


def clear_threads(context: GraphQLContext, threads: Iterable[Thread]):
    loader = get_loader(context, "thread", get_threads_by_id)
    for thread in threads:
        loader.clear(thread.id)


def clear_all_threads(context: GraphQLContext):
    loader = get_loader(context, "thread", get_threads_by_id)
    loader.clear_all()
