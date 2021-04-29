import random
from datetime import datetime
from typing import Optional

from misago.categories.models import Category
from misago.threads.models import Post, Thread
from misago.users.models import User

from .richtext import create_fake_rich_text
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

    rich_text = create_fake_rich_text()

    return await Post.create(
        thread,
        markup,
        rich_text,
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
    thread = await Thread.create(
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

    thread = await thread.update(first_post=post, last_post=post)

    return thread
