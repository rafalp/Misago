from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .enums import SearchOrder
from .posts import posts_search


class CategoryProxy:
    id: int

    def __init__(self, id: int):
        self.id = id


def debug_search(request: HttpRequest) -> HttpResponse:
    query = (request.GET.get("q") or "").strip()
    mode = (request.GET.get("mode") or "").strip()
    sorting = (request.GET.get("sorting") or "").strip()

    categories = []
    for category in request.categories.category_list:
        categories.append(CategoryProxy(category["id"]))

    valid_modes = ("threads", "posts", "thread_titles")
    if mode not in valid_modes:
        mode = valid_modes[0]

    valid_sortings = ("relevance", "newest")
    if sorting not in valid_sortings:
        sorting = valid_sortings[0]

    if query:
        if mode == "threads":
            results = posts_search.search_threads(
                query,
                request.user_permissions,
                categories=categories,
                order_by=SearchOrder(sorting),
            )
        elif mode == "posts":
            results = posts_search.search_posts(
                query,
                request.user_permissions,
                categories=categories,
                order_by=SearchOrder(sorting),
            )
        elif mode == "thread_titles":
            results = posts_search.search_thread_titles(
                query,
                request.user_permissions,
                categories=categories,
                order_by=SearchOrder(sorting),
            )
    else:
        results = None

    return render(
        request,
        "misago/search/debug.html",
        {
            "query": query,
            "mode": mode,
            "sorting": sorting,
            "results": results,
        },
    )
