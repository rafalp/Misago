from typing import Awaitable, Sequence, Tuple

from ..users.models import User
from .models import Post, Thread
from .sync import sync_thread, sync_thread_by_id


def delete_thread_post(thread: Thread, post: Post) -> Awaitable[Tuple[Thread, Post]]:
    return delete_thread_posts(thread, [post])


async def delete_thread_posts(
    thread: Thread, posts: Sequence[Post]
) -> Tuple[Thread, Post]:
    posts_ids = [i.id for i in posts]
    posts_query = thread.posts_query.exclude(id__in=posts_ids)
    updated_thread, stats = await sync_thread(thread, posts_query)
    await thread.posts_query.filter(id__in=posts_ids).delete()
    return updated_thread, stats["last_post"]


def delete_user_threads(user: User):
    return user.threads_query.filter(starter_id=user.id).delete()


async def delete_user_posts(user: User):
    threads_ids_subquery = user.posts_query.distinct().subquery("poster_id")
    threads_to_update = Thread.query.filter(id__in=threads_ids_subquery)
    exclude_deleted_posts = Post.query.exclude(poster_id=user.id)

    async for thread in threads_to_update.batch("id"):
        await sync_thread_by_id(thread.id, exclude_deleted_posts)

    await user.posts_query.delete()
