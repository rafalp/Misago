import random
from datetime import datetime
from typing import Optional

from misago.types import Category, Post, Thread, User
from misago.threads.create import create_post, create_thread
from misago.threads.update import update_thread
from misago.utils.strings import get_random_string

from .sentences import Sentences


sentences = Sentences(max_length=200)


async def create_fake_post(
    thread: Thread,
    *,
    poster: Optional[User] = None,
    poster_name: Optional[str] = None,
    posted_at: Optional[datetime] = None,
) -> Post:
    texts = [sentences.get_random_sentence() for _ in range(random.randint(1, 15))]

    markup = "\n\n".join(texts)
    html = "<p>%s</p>" % "</p>\n\n<p>".join(texts)

    rich_text = [
        {"id": get_random_string(6), "type": "p", "text": text} for text in texts
    ]

    return await create_post(
        thread,
        markup,
        rich_text,
        html,
        poster=poster,
        poster_name=poster_name,
        posted_at=posted_at,
    )


async def create_fake_thread(
    category: Category,
    *,
    starter: Optional[User] = None,
    starter_name: Optional[str] = None,
    started_at: Optional[datetime] = None,
) -> Thread:
    thread = await create_thread(
        category,
        title=sentences.get_random_sentence(),
        starter=starter,
        starter_name=starter_name,
        started_at=started_at,
        is_closed=random.randint(0, 100) > 80,
    )

    post = await create_fake_post(
        thread, poster=starter, poster_name=starter_name, posted_at=thread.started_at
    )

    thread = await update_thread(thread, first_post=post, last_post=post)

    return thread
