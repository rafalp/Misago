from ..database.queries import delete
from ..tables import threads
from ..types import Thread


async def delete_thread(thread: Thread):
    await delete(threads, thread.id)
