from starlette.requests import Request

from .categories import categories_route
from .threads import threads_route


async def index_route(request: Request):
    """Simple router that renders either threads list or categories list"""
    if request.state.settings["forum_index_threads"]:
        return await threads_route(
            request,
            on_index=True,
            template_name="index_threads.html",
        )

    return await categories_route(
        request,
        on_index=True,
        template_name="index_categories.html",
    )
