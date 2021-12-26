from typing import List, Optional

from starlette.requests import Request

from ..categories.get import get_all_categories
from ..categories.models import Category
from ..template import render
from ..threads.get import get_threads_feed
from .exceptions import HTTPNotFound
from .utils import get_cursor_or_404, parse_id_or_404


async def category_route(request: Request):
    category_id = parse_id_or_404(request)
    categories = await get_all_categories()
    category = find_category_by_id(categories, category_id)
    child_categories = [
        node for node in categories if category.is_parent(node, include_self=True)
    ]

    cursor = get_cursor_or_404(request)
    threads = await get_threads_feed(
        request.state.settings["threads_per_page"],
        cursor or None,
        categories=child_categories,
    )

    if cursor and not threads.items:
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


def find_category_by_id(categories: List[Category], id: int) -> Category:
    categories_map = {category.id: category for category in categories}
    try:
        return categories_map[id]
    except KeyError:
        raise HTTPNotFound()
