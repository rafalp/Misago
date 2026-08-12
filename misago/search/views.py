from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .enums import SearchMode
from .posts import posts_search


class CategoryProxy:
    id: int

    def __init__(self, id: int):
        self.id = id


def debug_search(request: HttpRequest) -> HttpResponse:
    query = (request.GET.get("q") or "").strip()
    mode = (request.GET.get("mode") or "").strip()

    categories = []
    for category in request.categories.category_list:
        categories.append(CategoryProxy(category["id"]))

    valid_modes = ("threads", "posts", "thread_titles")
    if mode not in valid_modes:
        mode = valid_modes[0]

    if query:
        if mode == "threads":
            results = posts_search.search_threads(
                query, request.user_permissions, categories=categories
            )
        elif mode == "posts":
            results = posts_search.search_posts(
                query, request.user_permissions, categories=categories
            )
        elif mode == "thread_titles":
            results = posts_search.search_thread_titles(
                query, request.user_permissions, categories=categories
            )
    else:
        results = None

    return render(
        request,
        "misago/search/debug.html",
        {
            "query": query,
            "mode": mode,
            "results": results,
        },
    )
