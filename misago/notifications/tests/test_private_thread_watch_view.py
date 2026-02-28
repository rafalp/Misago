from django.urls import reverse

from ...test import assert_contains
from ..enums import ThreadNotifications
from ..models import WatchedThread
from ..threads import watch_thread


def test_private_thread_watch_view_creates_new_watched_thread_with_emails_on_post(
    user_client, user, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.SITE_AND_EMAIL},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
        },
    )

    watched_thread = WatchedThread.objects.get(
        user=user, thread=other_user_private_thread
    )
    assert watched_thread.send_emails


def test_private_thread_watch_view_creates_new_watched_thread_with_emails_on_post_in_htmx(
    user_client, user, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.SITE_AND_EMAIL},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watched")

    watched_thread = WatchedThread.objects.get(
        user=user, thread=other_user_private_thread
    )
    assert watched_thread.send_emails


def test_private_thread_watch_view_creates_new_watched_thread_with_emails_for_watched_thread_on_post(
    user_client, user, other_user_private_thread
):
    watch_thread(other_user_private_thread, user, send_emails=False)

    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.SITE_AND_EMAIL},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
        },
    )

    watched_thread = WatchedThread.objects.get(
        user=user, thread=other_user_private_thread
    )
    assert watched_thread.send_emails


def test_private_thread_watch_view_creates_new_watched_thread_with_emails_for_watched_thread_on_post_in_htmx(
    user_client, user, other_user_private_thread
):
    watch_thread(other_user_private_thread, user, send_emails=False)

    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.SITE_AND_EMAIL},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watched")

    watched_thread = WatchedThread.objects.get(
        user=user, thread=other_user_private_thread
    )
    assert watched_thread.send_emails


def test_private_thread_watch_view_creates_new_watched_thread_with_emails_for_watched_thread_with_emails_on_post(
    user_client, user, other_user_private_thread
):
    watch_thread(other_user_private_thread, user, send_emails=True)

    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.SITE_AND_EMAIL},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
        },
    )

    watched_thread = WatchedThread.objects.get(
        user=user, thread=other_user_private_thread
    )
    assert watched_thread.send_emails


def test_private_thread_watch_view_creates_new_watched_thread_with_emails_for_watched_thread_with_emails_on_post_in_htmx(
    user_client, user, other_user_private_thread
):
    watch_thread(other_user_private_thread, user, send_emails=True)

    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.SITE_AND_EMAIL},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watched")

    watched_thread = WatchedThread.objects.get(
        user=user, thread=other_user_private_thread
    )
    assert watched_thread.send_emails


def test_private_thread_watch_view_creates_new_watched_thread_without_emails_on_post(
    user_client, user, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.SITE_ONLY},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
        },
    )

    watched_thread = WatchedThread.objects.get(
        user=user, thread=other_user_private_thread
    )
    assert not watched_thread.send_emails


def test_private_thread_watch_view_creates_new_watched_thread_without_emails_on_post_in_htmx(
    user_client, user, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.SITE_ONLY},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watched")

    watched_thread = WatchedThread.objects.get(
        user=user, thread=other_user_private_thread
    )
    assert not watched_thread.send_emails


def test_private_thread_watch_view_creates_new_watched_thread_without_emails_for_watched_thread_with_emails_on_post(
    user_client, user, other_user_private_thread
):
    watch_thread(other_user_private_thread, user, send_emails=True)

    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.SITE_ONLY},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
        },
    )

    watched_thread = WatchedThread.objects.get(
        user=user, thread=other_user_private_thread
    )
    assert not watched_thread.send_emails


def test_private_thread_watch_view_creates_new_watched_thread_without_emails_for_watched_thread_with_emails_on_post_in_htmx(
    user_client, user, other_user_private_thread
):
    watch_thread(other_user_private_thread, user, send_emails=True)

    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.SITE_ONLY},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watched")

    watched_thread = WatchedThread.objects.get(
        user=user, thread=other_user_private_thread
    )
    assert not watched_thread.send_emails


def test_private_thread_watch_view_creates_new_watched_thread_without_emails_for_watched_thread_on_post(
    user_client, user, other_user_private_thread
):
    watch_thread(other_user_private_thread, user, send_emails=False)

    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.SITE_ONLY},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
        },
    )

    watched_thread = WatchedThread.objects.get(
        user=user, thread=other_user_private_thread
    )
    assert not watched_thread.send_emails


def test_private_thread_watch_view_creates_new_watched_thread_without_emails_for_watched_thread_on_post_in_htmx(
    user_client, user, other_user_private_thread
):
    watch_thread(other_user_private_thread, user, send_emails=False)

    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.SITE_ONLY},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watched")

    watched_thread = WatchedThread.objects.get(
        user=user, thread=other_user_private_thread
    )
    assert not watched_thread.send_emails


def test_private_thread_watch_view_deletes_watched_thread_on_post(
    user_client, user, other_user_private_thread
):
    watch_thread(other_user_private_thread, user)

    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.NONE},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
        },
    )

    assert not WatchedThread.objects.exists()


def test_private_thread_watch_view_deletes_watched_thread_on_post_in_htmx(
    user_client, user, other_user_private_thread
):
    watch_thread(other_user_private_thread, user)

    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.NONE},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watch")

    assert not WatchedThread.objects.exists()


def test_private_thread_watch_view_does_nothing_for_unwatched_thread_on_post(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.NONE},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
        },
    )

    assert not WatchedThread.objects.exists()


def test_private_thread_watch_view_does_nothing_for_unwatched_thread_on_post_in_htmx(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {"notifications": ThreadNotifications.NONE},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watch")

    assert not WatchedThread.objects.exists()


def test_private_thread_watch_view_redirects_to_next_thread_url(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "notifications": ThreadNotifications.NONE,
            "next": reverse(
                "misago:private-thread",
                kwargs={
                    "thread_id": other_user_private_thread.id,
                    "slug": other_user_private_thread.slug,
                    "page": 21,
                },
            ),
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
            "page": 21,
        },
    )


def test_private_thread_watch_view_returns_error_403_if_user_is_anonymous(
    client, other_user_private_thread
):
    response = client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
    )
    assert_contains(
        response, "You must be signed in to watch threads.", status_code=403
    )


def test_private_thread_watch_view_returns_error_403_if_user_has_no_private_threads_permission(
    user_client, members_group, other_user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "You can&#x27;t use private threads.", status_code=403)


def test_private_thread_watch_view_returns_error_404_if_thread_doesnt_exist(
    user_client,
):
    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": 1,
                "slug": "doesnt-exist",
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_watch_view_returns_error_404_if_user_cant_see_thread(
    user_client, private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_watch_view_returns_error_404_if_its_thread(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:private-thread-watch",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        ),
    )
    assert response.status_code == 404
