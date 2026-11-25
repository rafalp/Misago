from django.http import HttpRequest

from ..search.quicksearch import get_quick_search_data


def quick_search(request: HttpRequest) -> dict:
    quick_search = get_quick_search_data(request)

    request.frontend_context["can_quick_search"] = bool(quick_search)

    return {"quick_search": quick_search}
