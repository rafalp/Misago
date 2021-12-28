from typing import List

from starlette.requests import Request
from starlette.responses import RedirectResponse

from ..categories.get import get_all_categories
from ..categories.models import Category
from ..template import render
from ..threads.get import get_threads_feed
from .exceptions import HTTPNotFound
from .utils import clean_cursor_or_404, clean_id_or_404


async def category_route(request: Request):
    category_id = clean_id_or_404(request)
    categories = await get_all_categories()
    category = find_category_by_id(categories, category_id)

    if category.slug != request.path_params["slug"]:
        return get_category_redirect(request, category)

    child_categories = [
        node for node in categories if category.is_parent(node, include_self=True)
    ]

    cursor = clean_cursor_or_404(request)
    threads = await get_threads_feed(
        request.state.settings["threads_per_page"],
        cursor or None,
        categories=child_categories,
    )

    if cursor and not threads.items:
        print("NO ITEMS")
        raise HTTPNotFound()

    return await render(
        request,
        "category.html",
        {
            "category": category,
            "categories": child_categories[1:],
            "threads": threads,
        },
    )


def find_category_by_id(categories: List[Category], category_id: int) -> Category:
    categories_map = {category.id: category for category in categories}
    try:
        return categories_map[category_id]
    except KeyError as exception:
        raise HTTPNotFound() from exception


def get_category_redirect(request: Request, category: Category) -> RedirectResponse:
    url = request.url_for("category", slug=category.slug, id=category.id)
    return RedirectResponse(url, 301)
