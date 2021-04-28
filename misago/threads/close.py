from dataclasses import replace
from typing import List, Sequence

from ..database import database
from ..tables import threads as threads_table
from .models import Thread
from .update import update_thread


async def close_thread(thread: Thread, is_closed: bool) -> Thread:
    return await update_thread(thread, is_closed=is_closed)


async def close_threads(threads: Sequence[Thread], is_closed: bool) -> List[Thread]:
    updated_threads: List[Thread] = []
    db_update: List[int] = []

    for thread in threads:
        if thread.is_closed != is_closed:
            thread = replace(thread, is_closed=is_closed)
            db_update.append(thread.id)
        updated_threads.append(thread)

    if db_update:
        update_threads_query = (
            threads_table.update(None)
            .values(is_closed=is_closed)
            .where(threads_table.c.id.in_(db_update))
        )
        await database.execute(update_threads_query),

    return updated_threads
