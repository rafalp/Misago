from starlette.requests import Request

from ..template import render
from ..threads.get import get_threads_feed
from .exceptions import HTTPNotFound
from .utils import clean_cursor_or_404


async def threads_route(
    request: Request, *, on_index: bool = False, template_name: str = "threads.html"
):
    if not on_index and request.state.settings["forum_index_threads"]:
        raise HTTPNotFound()

    cursor = clean_cursor_or_404(request)
    threads = await get_threads_feed(
        request.state.settings["threads_per_page"],
        cursor or None,
    )

    if cursor and not threads.items:
        raise HTTPNotFound()

    return await render(request, template_name, {"threads": threads})
