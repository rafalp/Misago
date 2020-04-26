from ..types import Thread
from .broadcast import broadcast


THREADS_CHANNEL = "threads_updates"


async def publish_thread_update(thread: Thread):
    await broadcast.publish(channel=THREADS_CHANNEL, message=str(thread.id))


async def threads_updates():
    async with broadcast.subscribe(channel=THREADS_CHANNEL) as subscriber:
        async for event in subscriber:
            yield int(event.message)
