from typing import List, Optional

from starlette.requests import Request
from starlette.responses import RedirectResponse

from ..categories.get import get_all_categories
from ..graphql.connection import Connection
from ..template import render
from ..threads.models import Thread
from .exceptions import HTTPNotFound
from .utils import clean_cursor_or_404

threads_connection = Connection("-last_post_id")


async def threads_route(
    request: Request, *, on_index: bool = False, template_name: str = "threads.html"
):
    if not on_index and request.state.settings["forum_index_threads"]:
        raise HTTPNotFound()

    categories = await get_all_categories()

    return await base_threads_route(
        request,
        template_name,
        [category.id for category in categories],
    )


async def base_threads_route(
    request: Request,
    template_name: str,
    categories_ids: List[int],
    context: Optional[dict] = None,
):
    after, before = clean_cursor_or_404(request)
    threads_query = Thread.query.filter(category_id__in=categories_ids)

    threads = await threads_connection.resolve(
        context,
        threads_query,
        {
            "first": request.state.settings["threads_per_page"],
            "after": after,
            "before": before,
        },
        request.state.settings["threads_per_page"],
    )

    if (after or before) and not threads.edges:
        raise HTTPNotFound()

    if before:
        if not threads.page_info.has_previous_page:
            # On explicit first page of threads redirect user to page without cursor
            return RedirectResponse(request.base_url)

        if len(threads.edges) < request.state.settings["threads_per_page"]:
            # On partial first page of threads redirect user to page without cursor
            return RedirectResponse(request.base_url)

    context = context or {}
    context["threads"] = threads

    return await render(request, template_name, context)
