from starlette.requests import Request

from ..categories.get import get_all_categories
from ..template import render
from .exceptions import HTTPNotFound


async def categories_route(
    request: Request, *, on_index: bool = False, template_name: str = "categories.html"
):
    if not on_index and not request.state.settings["forum_index_threads"]:
        raise HTTPNotFound()

    categories = await get_all_categories()

    return await render(request, template_name, {"categories": categories})
