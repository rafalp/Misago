from datetime import datetime
from typing import Optional

from misago.types import Category, Post, Thread, User
from misago.threads.create import create_post, create_thread
from misago.threads.update import update_thread

from .sentences import Sentences


sentences = Sentences(max_length=200)


async def create_fake_post(
    thread: Thread,
    *,
    poster: Optional[User] = None,
    poster_name: Optional[str] = None,
    posted_at: Optional[datetime] = None,
) -> Post:
    return await create_post(
        thread,
        body={"text": sentences.get_random_sentence()},
        poster=poster,
        poster_name=poster_name,
        posted_at=posted_at,
    )


async def create_fake_thread(
    category: Category,
    *,
    starter: Optional[User] = None,
    starter_name: Optional[str] = None,
    is_closed: bool = False,
    started_at: Optional[datetime] = None,
) -> Thread:
    thread = await create_thread(
        category,
        title=sentences.get_random_sentence(),
        starter=starter,
        starter_name=starter_name,
        is_closed=is_closed,
        started_at=started_at,
    )

    post = await create_fake_post(
        thread, poster=starter, poster_name=starter_name, posted_at=thread.started_at
    )

    thread = await update_thread(thread, first_post=post, last_post=post)

    return thread
