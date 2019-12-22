from asyncio import gather

from ..database import database
from ..tables import posts
from ..types import Category, Thread
from .update import update_thread


async def move_thread(thread: Thread, new_category: Category) -> Thread:
    if thread.category_id == new_category.id:
        return thread

    move_posts_query = (
        posts.update(None)
        .values(category_id=new_category.id)
        .where(posts.c.thread_id == thread.id)
    )

    thread, _ = await gather(
        update_thread(thread, category=new_category),
        database.execute(move_posts_query),
    )

    return thread
