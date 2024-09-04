from django.urls import reverse

from ..models import Thread
from ..threadurl import get_thread_url


def test_get_thread_url_returns_thread_url(django_assert_num_queries, thread):
    with django_assert_num_queries(0):
        url = get_thread_url(thread)

    assert url == reverse(
        "misago:thread", kwargs={"id": thread.id, "slug": thread.slug}
    )


def test_get_thread_url_returns_thread_url_using_category_arg(
    django_assert_num_queries, thread, default_category
):
    thread_without_related = Thread.objects.get(id=thread.id)
    with django_assert_num_queries(0):
        url = get_thread_url(thread_without_related, default_category)

    assert url == reverse(
        "misago:thread", kwargs={"id": thread.id, "slug": thread.slug}
    )


def test_get_thread_url_returns_private_thread_url(
    django_assert_num_queries, private_thread
):
    with django_assert_num_queries(0):
        url = get_thread_url(private_thread)

    assert url == reverse(
        "misago:private-thread",
        kwargs={"id": private_thread.id, "slug": private_thread.slug},
    )


def test_get_thread_url_returns_private_thread_url_using_category(
    django_assert_num_queries, private_thread, private_threads_category
):
    thread_without_related = Thread.objects.get(id=private_thread.id)
    with django_assert_num_queries(0):
        url = get_thread_url(thread_without_related, private_threads_category)

    assert url == reverse(
        "misago:private-thread",
        kwargs={"id": private_thread.id, "slug": private_thread.slug},
    )
