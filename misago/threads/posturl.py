from ..conf.types import Settings
from .get import get_thread_posts_paginator
from .models import Thread


async def get_thread_post_url(settings: Settings, thread: Thread, post_id: int) -> str:
    page_number = await get_thread_post_page(settings, thread, post_id)

    url = f"/t/{thread.slug}/{thread.id}/"
    if page_number > 1:
        url += f"{page_number}/"
    url += f"#post-{post_id}"
    return url


async def get_thread_post_page(settings: Settings, thread: Thread, post_id: int) -> int:
    paginator = await get_thread_posts_paginator(
        thread,
        settings["posts_per_page"],
        settings["posts_per_page_orphans"],
    )

    post_position_query = await thread.posts_query.filter(id__lte=post_id).count()
    return await paginator.get_page_number_for_offset(post_position_query)
