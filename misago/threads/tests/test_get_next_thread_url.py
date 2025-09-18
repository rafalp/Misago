from django.urls import resolve, reverse

from ..nexturl import get_next_thread_url


def test_get_next_thread_url_returns_thread_url_from_request_resolve_match(rf, thread):
    request = rf.get("/t/lorem-ipsum/123/")
    request.resolver_match = resolve("/t/lorem-ipsum/123/")

    next_url = get_next_thread_url(request, thread, "misago:thread")
    assert next_url == "/t/lorem-ipsum/123/"


def test_get_next_thread_url_returns_thread_url_from_request_resolve_match_with_page(
    rf, thread
):
    request = rf.get("/t/lorem-ipsum/123/8/")
    request.resolver_match = resolve("/t/lorem-ipsum/123/8/")

    next_url = get_next_thread_url(request, thread, "misago:thread")
    assert next_url == "/t/lorem-ipsum/123/8/"


def test_get_next_thread_url_returns_thread_url_if_request_resolve_match_is_not_thread(
    rf, thread
):
    request = rf.get("/u/john/123/")
    request.resolver_match = resolve("/u/john/123/")

    next_url = get_next_thread_url(request, thread, "misago:thread")
    assert next_url == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )


def test_get_next_thread_url_returns_thread_url_from_request_post_next_value(
    rf, thread
):
    thread_url = reverse(
        "misago:thread",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
        },
    )

    request = rf.post("/u/john/123/", {"next": thread_url})
    request.resolver_match = resolve("/u/john/123/")

    next_url = get_next_thread_url(request, thread, "misago:thread")
    assert next_url == thread_url


def test_get_next_thread_url_returns_thread_page_url_from_request_post_next_value(
    rf, thread
):
    thread_url = reverse(
        "misago:thread",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
            "page": 21,
        },
    )

    request = rf.post("/u/john/123/", {"next": thread_url})
    request.resolver_match = resolve("/u/john/123/")

    next_url = get_next_thread_url(request, thread, "misago:thread")
    assert next_url == thread_url


def test_get_next_thread_url_returns_thread_url_from_resolver_match_if_post_next_value_is_not_thread_url(
    rf, thread
):
    thread_url = reverse(
        "misago:thread",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
            "page": 21,
        },
    )

    request = rf.post(thread_url, {"next": "/c/test/123"})
    request.resolver_match = resolve(thread_url)

    next_url = get_next_thread_url(request, thread, "misago:thread")
    assert next_url == thread_url


def test_get_next_thread_url_returns_thread_url_if_resolver_match_and_post_next_value_is_not_thread_url(
    rf, thread
):
    request = rf.post("/u/john/123/", {"next": "/c/test/123"})
    request.resolver_match = resolve("/u/john/123/")

    next_url = get_next_thread_url(request, thread, "misago:thread")
    assert next_url == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )
