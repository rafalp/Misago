from typing import Awaitable, Optional, Sequence, Union

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
