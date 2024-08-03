from urllib.parse import urlparse

from django.http import HttpRequest
from django.urls import Resolver404, resolve
from django.utils.http import url_has_allowed_host_and_scheme

NEXT_PAGE = "next"


def get_next_page_url(request: HttpRequest) -> str | None:
    redirect_to = request.POST.get(NEXT_PAGE, request.GET.get(NEXT_PAGE))
    if redirect_to:
        return clean_next_page_url(request, redirect_to)
    return None


def clean_next_page_url(request: HttpRequest, redirect_to: str) -> str | None:
    url_is_safe = url_has_allowed_host_and_scheme(
        url=redirect_to,
        allowed_hosts=request.get_host(),
        require_https=request.is_secure(),
    )

    if not url_is_safe:
        return None

    path, query = parse_redirect_url(redirect_to)
    if not path:
        return None

    try:
        resolve(path)
        return build_redirect_url(path, query)
    except Resolver404:
        return None


def parse_redirect_url(redirect_to: str) -> tuple[str, str] | None:
    try:
        parsed = urlparse(redirect_to)
        return parsed.path, parsed.query
    except ValueError:
        return None


def build_redirect_url(path: str, query: str) -> str:
    redirect_url = path
    if query:
        redirect_url += f"?{query}"
    return redirect_url
