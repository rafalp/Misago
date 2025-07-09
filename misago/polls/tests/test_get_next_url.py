from django.urls import resolve

from ..nexturl import get_next_url


def test_get_next_url_returns_thread_url_from_request_resolve_match(rf, thread):
    request = rf.get("/t/lorem-ipsum/123/")
    request.resolver_match = resolve("/t/lorem-ipsum/123/")

    next_url = get_next_url(request, thread)
    assert next_url == "/t/lorem-ipsum/123/"


def test_get_next_url_returns_thread_url_from_request_resolve_match_with_page(
    rf, thread
):
    request = rf.get("/t/lorem-ipsum/123/8/")
    request.resolver_match = resolve("/t/lorem-ipsum/123/8/")

    next_url = get_next_url(request, thread)
    assert next_url == "/t/lorem-ipsum/123/8/"
