from typing import List

from starlette.requests import Request

from ..categories.get import get_all_categories
from ..categories.models import Category
from ..template import render
from ..threads.get import get_thread_posts_page, get_threads_by_id
from ..threads.models import Thread
from .exceptions import HTTPNotFound
from .utils import get_cursor_or_404, parse_id_or_404


async def thread_route(request: Request):
    thread_id = parse_id_or_404(request)
    thread = await get_thread_or_404(thread_id)
    path = await get_thread_path(thread.category_id)

    return await render(
        request,
        "thread.html",
        {
            "category": path[-1],
            "thread": thread,
            "path": path,
        },
    )


async def get_thread_or_404(thread_id: int) -> Thread:
    threads = await get_threads_by_id([thread_id])
    try:
        return threads[0]
    except IndexError:
        raise HTTPNotFound()


async def get_thread_path(category_id: int) -> List[Category]:
    categories = await get_all_categories()
    category = {item.id: item for item in categories}[category_id]
    return [node for node in categories if node.is_parent(category, include_self=True)]
