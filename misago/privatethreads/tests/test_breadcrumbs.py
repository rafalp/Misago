from django.urls import reverse

from ..breadcrumbs import (
    get_private_thread_breadcrumbs,
    get_private_threads_breadcrumbs,
)


def test_get_private_threads_breadcrumbs_returns_private_threads_list_breadcrumbs():
    data = get_private_threads_breadcrumbs(None)

    assert data == {
        "id": "breadcrumbs",
        "template_name": "misago/private_threads_breadcrumbs.html",
        "items": [
            {
                "type": "private_threads",
                "label": "Private threads",
                "url": reverse("misago:private-thread-list"),
            },
        ],
    }


def test_get_private_thread_breadcrumbs_returns_thread_breadcrumbs(private_thread):
    data = get_private_thread_breadcrumbs(None, private_thread)

    assert data == {
        "id": "breadcrumbs",
        "template_name": "misago/private_thread_breadcrumbs.html",
        "items": [
            {
                "type": "private_threads",
                "label": "Private threads",
                "url": reverse("misago:private-thread-list"),
            },
            {
                "type": "private_thread",
                "label": private_thread.title,
                "url": reverse(
                    "misago:private-thread",
                    kwargs={
                        "thread_id": private_thread.id,
                        "slug": private_thread.slug,
                    },
                ),
            },
        ],
    }
