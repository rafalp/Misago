from typing import Sequence

from ..database.queries import delete, delete_many
from ..tables import threads as threads_table
from ..types import Thread


async def delete_thread(thread: Thread):
    await delete(threads_table, thread.id)


async def delete_threads(threads: Sequence[Thread]):
    await delete_many(threads_table, [t.id for t in threads])
