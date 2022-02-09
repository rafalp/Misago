from typing import Awaitable, Iterable, Optional

from ..context import Context
from ..loaders import Loader, batch_load_function, simple_loader
from ..database.paginator import Paginator
from .get import (
    get_posts_by_id,
    get_threads_by_id,
    get_thread_posts_paginator,
)
from .models import Post, Thread, ThreadsFeed
from .posturl import get_thread_post_url

batch_load_posts = batch_load_function(get_posts_by_id)
batch_load_threads = batch_load_function(get_threads_by_id)


class ThreadsLoader(Loader[Thread]):
    context_key = "_threads_loader"

    def get_batch_load_function(self):
        return batch_load_threads


threads_loader = ThreadsLoader()


class PostsLoader(Loader[Post]):
    context_key = "_posts_loader"

    def get_batch_load_function(self):
        return batch_load_posts

    def unload_with_thread_id(self, context: Context, thread_id: int):
        self.unload_by_attr_value(context, "thread_id", int(thread_id))

    def unload_with_thread_id_in(self, context: Context, threads_ids: Iterable[int]):
        threads_ids = [int(thread_id) for thread_id in threads_ids]
        self.unload_by_attr_value_in(context, "thread_id", threads_ids)

    def load_paginator(
        self, context: Context, thread_id: int
    ) -> Awaitable[Optional[Paginator]]:
        return load_posts_paginator(context, thread_id=thread_id)

    def load_url(self, context: Context, post: Post) -> Awaitable[Optional[str]]:
        return load_post_url(context, thread_id=post.thread_id, post_id=post.id)


posts_loader = PostsLoader()


@simple_loader("post_url")
async def load_post_url(
    context: Context,
    *,
    thread_id: int,
    post_id: int,
):
    thread = await threads_loader.load(context, thread_id)
    return await get_thread_post_url(context["settings"], thread, post_id)


@simple_loader("thread_posts")
async def load_posts_paginator(
    context: Context, *, thread_id: int
) -> Awaitable[Optional[Paginator]]:
    thread = await threads_loader.load(context, thread_id)
    if not thread:
        return None

    return await get_thread_posts_paginator(
        thread,
        per_page=context["settings"]["posts_per_page"],
        orphans=context["settings"]["posts_per_page_orphans"],
    )
