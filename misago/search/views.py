from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .enums import SearchMode
from .posts import posts_search


def debug_search(request: HttpRequest) -> HttpResponse:
    query = (request.GET.get("q") or "").strip()
    if query:
        results = posts_search.search(
            query, SearchMode.THREADS, permissions=request.user_permissions
        )
    else:
        results = None

    return render(
        request,
        "misago/search/debug.html",
        {
            "query": query,
            "results": results,
        },
    )
