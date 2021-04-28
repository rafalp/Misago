from asyncio import gather
from typing import Iterable, Sequence, Tuple, cast

from sqlalchemy import and_, desc, not_

from ..categories.models import Category
from ..database import database
from ..database.queries import count, delete, delete_many
from ..tables import posts as posts_table
from ..tables import threads as threads_table
from ..users.models import User
from .models import Post, Thread
from .update import update_thread


async def delete_thread(thread: Thread):
    await delete(threads_table, thread.id)


async def delete_threads(threads: Iterable[Thread]):
    await delete_many(threads_table, [i.id for i in threads])


async def delete_thread_post(thread: Thread, post: Post) -> Tuple[Thread, Post]:
    return await delete_thread_posts(thread, [post])


async def delete_thread_posts(
    thread: Thread, posts: Sequence[Post]
) -> Tuple[Thread, Post]:
    posts_ids = [i.id for i in posts]
    posts_count_query = count(
        posts_table.select(None).where(
            and_(
                posts_table.c.thread_id == thread.id,
                not_(posts_table.c.id.in_(posts_ids)),
            )
        )
    )
    last_reply_query = (
        posts_table.select(None)
        .where(
            and_(
                posts_table.c.thread_id == thread.id,
                not_(posts_table.c.id.in_(posts_ids)),
            )
        )
        .order_by(desc(posts_table.c.id))
        .limit(1)
    )
    posts_count, last_post_data = await gather(
        posts_count_query,
        database.fetch_one(last_reply_query),
    )

    last_post = Post(**cast(dict, last_post_data))

    updated_thread = await update_thread(
        thread,
        replies=posts_count - 1,  # first post doesnt count to replies,
        last_post=last_post,
    )

    await delete_many(posts_table, posts_ids)

    return updated_thread, last_post


async def delete_threads_in_categories(categories: Iterable[Category]):
    query = threads_table.delete(None).where(
        threads_table.c.category_id.in_([c.id for c in categories])
    )
    await database.execute(query)


async def delete_user_threads(user: User):
    query = threads_table.delete(None).where(threads_table.c.user_id == user.id)
    await database.execute(query)


async def delete_user_posts(user: User):
    query = threads_table.delete(None).where(threads_table.c.user_id == user.id)
    await database.execute(query)
