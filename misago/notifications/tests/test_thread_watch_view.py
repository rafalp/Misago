from django.urls import reverse

from ...test import assert_contains
from ..enums import ThreadNotifications
from ..models import WatchedThread
from ..threads import watch_thread


def test_thread_watch_view_creates_new_watched_thread_with_emails_on_post(
    user_client, user, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.SITE_AND_EMAIL},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.send_emails


def test_thread_watch_view_creates_new_watched_thread_with_emails_on_post_in_htmx(
    user_client, user, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.SITE_AND_EMAIL},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watched")

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.send_emails


def test_thread_watch_view_creates_new_watched_thread_with_emails_for_watched_thread_on_post(
    user_client, user, thread
):
    watch_thread(thread, user, send_emails=False)

    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.SITE_AND_EMAIL},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.send_emails


def test_thread_watch_view_creates_new_watched_thread_with_emails_for_watched_thread_on_post_in_htmx(
    user_client, user, thread
):
    watch_thread(thread, user, send_emails=False)

    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.SITE_AND_EMAIL},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watched")

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.send_emails


def test_thread_watch_view_creates_new_watched_thread_with_emails_for_watched_thread_with_emails_on_post(
    user_client, user, thread
):
    watch_thread(thread, user, send_emails=True)

    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.SITE_AND_EMAIL},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.send_emails


def test_thread_watch_view_creates_new_watched_thread_with_emails_for_watched_thread_with_emails_on_post_in_htmx(
    user_client, user, thread
):
    watch_thread(thread, user, send_emails=True)

    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.SITE_AND_EMAIL},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watched")

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.send_emails


def test_thread_watch_view_creates_new_watched_thread_without_emails_on_post(
    user_client, user, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.SITE_ONLY},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert not watched_thread.send_emails


def test_thread_watch_view_creates_new_watched_thread_without_emails_on_post_in_htmx(
    user_client, user, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.SITE_ONLY},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watched")

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert not watched_thread.send_emails


def test_thread_watch_view_creates_new_watched_thread_without_emails_for_watched_thread_with_emails_on_post(
    user_client, user, thread
):
    watch_thread(thread, user, send_emails=True)

    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.SITE_ONLY},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert not watched_thread.send_emails


def test_thread_watch_view_creates_new_watched_thread_without_emails_for_watched_thread_with_emails_on_post_in_htmx(
    user_client, user, thread
):
    watch_thread(thread, user, send_emails=True)

    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.SITE_ONLY},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watched")

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert not watched_thread.send_emails


def test_thread_watch_view_creates_new_watched_thread_without_emails_for_watched_thread_on_post(
    user_client, user, thread
):
    watch_thread(thread, user, send_emails=False)

    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.SITE_ONLY},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert not watched_thread.send_emails


def test_thread_watch_view_creates_new_watched_thread_without_emails_for_watched_thread_on_post_in_htmx(
    user_client, user, thread
):
    watch_thread(thread, user, send_emails=False)

    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.SITE_ONLY},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watched")

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert not watched_thread.send_emails


def test_thread_watch_view_deletes_watched_thread_on_post(user_client, user, thread):
    watch_thread(thread, user)

    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.NONE},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    assert not WatchedThread.objects.exists()


def test_thread_watch_view_deletes_watched_thread_on_post_in_htmx(
    user_client, user, thread
):
    watch_thread(thread, user)

    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.NONE},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watch")

    assert not WatchedThread.objects.exists()


def test_thread_watch_view_does_nothing_for_unwatched_thread_on_post(
    user_client, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.NONE},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    assert not WatchedThread.objects.exists()


def test_thread_watch_view_does_nothing_for_unwatched_thread_on_post_in_htmx(
    user_client, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {"notifications": ThreadNotifications.NONE},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Watch")

    assert not WatchedThread.objects.exists()


def test_thread_watch_view_redirects_to_next_thread_url(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
        {
            "notifications": ThreadNotifications.NONE,
            "next": reverse(
                "misago:thread",
                kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 21},
            ),
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 21},
    )
