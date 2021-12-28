from starlette.requests import Request

from ..categories.get import get_all_categories
from ..template import render
from ..threads.get import get_threads_feed
from .exceptions import HTTPNotFound
from .utils import clean_cursor_or_404


async def index_route(request: Request):
    """Simple router that renders either threads list or categories list"""
    cursor = clean_cursor_or_404(request)
    threads = await get_threads_feed(
        request.state.settings["threads_per_page"],
        cursor or None,
    )

    if cursor and not threads.items:
        raise HTTPNotFound()

    categories = await get_all_categories()

    return await render(
        request, "index.html", {"categories": categories, "threads": threads}
    )
