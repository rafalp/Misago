from typing import List

from starlette.requests import Request
from starlette.responses import RedirectResponse

from ..categories.get import get_all_categories
from ..categories.models import Category
from ..template import render
from ..threads.get import (
    get_thread_posts_page,
    get_thread_posts_paginator,
    get_threads_by_id,
)
from ..threads.models import Thread
from .exceptions import HTTPNotFound
from .utils import ExplicitFirstPage, clean_id_or_404, clean_page_number_or_404


async def thread_route(request: Request):
    thread_id = clean_id_or_404(request)
    thread = await get_thread_or_404(thread_id)

    if thread.slug != request.path_params["slug"]:
        return get_thread_redirect(request, thread)

    path = await get_thread_path(thread.category_id)

    paginator = await get_thread_posts_paginator(
        thread,
        request.state.settings["posts_per_page"],
        request.state.settings["posts_per_page_orphans"],
    )

    try:
        page_number = clean_page_number_or_404(request)
    except ExplicitFirstPage:
        return get_thread_redirect(request, thread)

    posts = await get_thread_posts_page(paginator, page_number or 1)
    if not posts:
        raise HTTPNotFound()

    return await render(
        request,
        "thread.html",
        {
            "category": path[-1],
            "thread": thread,
            "path": path,
            "posts": posts,
        },
    )


async def get_thread_or_404(thread_id: int) -> Thread:
    threads = await get_threads_by_id([thread_id])
    try:
        return threads[0]
    except IndexError as exception:
        raise HTTPNotFound() from exception


def get_thread_redirect(request: Request, thread: Thread) -> RedirectResponse:
    url = request.url_for("thread", slug=thread.slug, id=thread.id)
    if request.path_params.get("page", 0) > 1:
        url += "%s/" % request.path_params["page"]
    return RedirectResponse(url, 301)


async def get_thread_path(category_id: int) -> List[Category]:
    categories = await get_all_categories()
    category = {item.id: item for item in categories}[category_id]
    return [node for node in categories if node.is_parent(category, include_self=True)]
