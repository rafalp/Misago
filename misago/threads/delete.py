from asyncio import gather
from typing import Iterable, Sequence, Tuple

from ..categories.models import Category
from ..users.models import User
from .models import Post, Thread


async def delete_thread_post(thread: Thread, post: Post) -> Tuple[Thread, Post]:
    return await delete_thread_posts(thread, [post])


async def delete_thread_posts(
    thread: Thread, posts: Sequence[Post]
) -> Tuple[Thread, Post]:
    posts_ids = [i.id for i in posts]
    posts_count_query = thread.posts_query.exclude(id__in=posts_ids).count()
    last_reply_query = (
        thread.posts_query.exclude(id__in=posts_ids).order_by("-id").stop(1).one()
    )

    posts_count, last_post = await gather(
        posts_count_query,
        last_reply_query,
    )

    updated_thread = await thread.update(
        replies=posts_count - 1,  # first post doesnt count to replies,
        last_post=last_post,
    )

    await thread.posts_query.filter(id__in=posts_ids).delete()

    return updated_thread, last_post


def delete_threads_in_categories(categories: Iterable[Category]):
    return Thread.query.filter(category_id__in=[c.id for c in categories]).delete()


def delete_user_threads(user: User):
    return Thread.query.filter(user_id=user.id).delete()


def delete_user_posts(user: User):
    return Post.query.filter(user_id=user.id).delete()
