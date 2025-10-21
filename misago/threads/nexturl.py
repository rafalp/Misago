from django.http import HttpRequest
from django.urls import Resolver404, resolve, reverse

from .models import Thread

NEXT_PAGE = "next"


def get_next_thread_url(
    request: HttpRequest, thread: Thread, url_name: str, strip_qs: bool = False
) -> str:
    """
    Attempt to return an absolute URL to a thread based on either the POST or GET
    query dict, falling back to absolute url if unavailable.
    """
    if request.method == "POST":
        if next_url := _get_next_thread_url_from_query_dict(
            request.POST, url_name, strip_qs
        ):
            return next_url

    if next_url := _get_next_thread_url_from_query_dict(
        request.GET, url_name, strip_qs
    ):
        return next_url

    resolved_url_name = request.resolver_match.url_name
    if request.resolver_match.namespace:
        resolved_url_name = f"{request.resolver_match.namespace}:{resolved_url_name}"

    if resolved_url_name == url_name:
        return request.path

    return reverse(url_name, kwargs={"thread_id": thread.id, "slug": thread.slug})


def _get_next_thread_url_from_query_dict(
    query_dict: dict, url_name: str, strip_qs: bool
) -> str | None:
    next_url = query_dict.get(NEXT_PAGE, "").strip()
    if not next_url:
        return None

    next_url_path = next_url
    if "?" in next_url_path:
        next_url_path = next_url_path[: next_url_path.index("?")]

    try:
        resolver_match = resolve(next_url_path)
    except Resolver404:
        return None

    resolved_url_name = resolver_match.url_name
    if resolver_match.namespace:
        resolved_url_name = f"{resolver_match.namespace}:{resolved_url_name}"

    if resolved_url_name != url_name:
        return None

    if strip_qs:
        return next_url_path

    return next_url
