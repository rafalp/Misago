from django.http import Http404, HttpRequest
from django.urls import resolve, reverse

from ..threads.models import Thread


def get_next_url(request: HttpRequest, thread: Thread) -> str:
    if next_url := get_next_url_from_post(request):
        return next_url

    if (
        request.resolver_match.namespace == "misago"
        and request.resolver_match.url_name == "thread"
    ):
        return request.path

    return reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})


def get_next_url_from_post(request: HttpRequest) -> str | None:
    if not request.method == "POST":
        return None

    next_url = request.POST.get("next")
    if not next_url:
        return None

    try:
        resolved_url = resolve(next_url)
    except Http404:
        return None

    url_name = resolved_url.url_name
    if resolved_url.namespace:
        url_name = f"{resolved_url.namespace}:{url_name}"
    if url_name != "misago:thread":
        return None

    if "?" in next_url:
        return next_url[: next_url.index("?")]

    return next_url
