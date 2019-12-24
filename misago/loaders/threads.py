from typing import Awaitable, Iterable, Optional, Sequence, Union

from ..types import GraphQLContext, Thread
from ..threads.get import get_threads_by_id
from .loader import get_loader


def load_thread(
    context: GraphQLContext, thread_id: Union[int, str]
) -> Awaitable[Optional[Thread]]:
    loader = get_loader(context, "thread_loader", get_threads_by_id)
    return loader.load(thread_id)


def load_threads(
    context: GraphQLContext, ids: Sequence[Union[int, str]]
) -> Awaitable[Sequence[Optional[Thread]]]:
    loader = get_loader(context, "thread_loader", get_threads_by_id)
    return loader.load_many(ids)


def store_thread(context: GraphQLContext, thread: Thread):
    loader = get_loader(context, "thread_loader", get_threads_by_id)
    loader.clear(thread.id)
    loader.prime(thread.id, thread)


def store_threads(context: GraphQLContext, threads: Iterable[Thread]):
    loader = get_loader(context, "thread_loader", get_threads_by_id)
    for thread in threads:
        loader.clear(thread.id)
        loader.prime(thread.id, thread)


def clear_thread(context: GraphQLContext, thread: Thread):
    loader = get_loader(context, "thread_loader", get_threads_by_id)
    loader.clear(thread.id)


def clear_threads(context: GraphQLContext):
    loader = get_loader(context, "thread_loader", get_threads_by_id)
    loader.clear_all()
