from asyncio import gather
from math import ceil
from typing import cast

from ..conf.types import Settings
from .models import Post, Thread


async def get_thread_post_url(settings: Settings, thread: Thread, post: Post) -> str:
    page_number = await get_thread_post_page(settings, thread, post)

    url = f"/t/{thread.slug}/{thread.id}/"
    if page_number > 1:
        url += f"/{page_number}/"
    url += f"#post-{post.id}"
    return url


async def get_thread_post_page(settings: Settings, thread: Thread, post: Post) -> int:
    thread_length_query = thread.posts_query.count()
    post_position_query = thread.posts_query.filter(id__lte=post.id).count()

    thread_length, post_position = await gather(
        thread_length_query, post_position_query
    )

    per_page = cast(int, settings["posts_per_page"]) - 1
    orphans = cast(int, settings["posts_per_page_orphans"])
    if orphans:
        orphans += 1

    hits = max(1, thread_length - orphans)
    thread_pages = int(ceil(hits / float(per_page)))

    if post_position >= thread_pages * per_page:
        return thread_pages

    return int(ceil(float(post_position) / (per_page)))
