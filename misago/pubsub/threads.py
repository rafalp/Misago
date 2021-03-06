import json

from ..types import Thread
from .broadcast import broadcast

THREADS_CHANNEL = "threads_updates"


def serialize_message(thread: Thread) -> str:
    return json.dumps({"id": thread.id, "category_id": thread.category_id})


async def publish_thread_update(thread: Thread):
    await broadcast.publish(channel=THREADS_CHANNEL, message=serialize_message(thread))


async def threads_updates():
    async with broadcast.subscribe(channel=THREADS_CHANNEL) as subscriber:
        async for event in subscriber:
            yield json.loads(event.message)
