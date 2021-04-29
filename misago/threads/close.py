from typing import Awaitable, List, Sequence

from .models import Thread


def close_thread(thread: Thread, is_closed: bool) -> Awaitable[Thread]:
    return thread.update(is_closed=is_closed)


async def close_threads(threads: Sequence[Thread], is_closed: bool) -> List[Thread]:
    updated_threads: List[Thread] = []
    threads_ids: List[int] = []

    for thread in threads:
        if thread.is_closed != is_closed:
            thread = thread.replace(is_closed=is_closed)
            threads_ids.append(thread.id)
        updated_threads.append(thread)

    if threads_ids:
        await Thread.query.filter(id__in=threads_ids).update(is_closed=is_closed)

    return updated_threads
