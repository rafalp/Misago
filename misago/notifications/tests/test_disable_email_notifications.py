from django.urls import reverse

from ..threads import ThreadNotifications


def test_disable_email_notifications_view_disables_emails_for_watched_thread(
    watched_thread_factory, user, user_client, thread
):
    watched_thread = watched_thread_factory(
        user, thread, ThreadNotifications.SEND_EMAIL
    )

    response = user_client.get(
        reverse(
            "misago:notifications-disable-email",
            kwargs={
                "watched_thread_id": watched_thread.id,
                "secret": watched_thread.secret,
            },
        )
    )
    assert response.status_code == 200

    watched_thread.refresh_from_db()
    assert watched_thread.notifications == ThreadNotifications.DONT_EMAIL


def test_disable_email_notifications_view_works_without_authentication(
    watched_thread_factory, user, client, thread
):
    watched_thread = watched_thread_factory(
        user, thread, ThreadNotifications.SEND_EMAIL
    )

    response = client.get(
        reverse(
            "misago:notifications-disable-email",
            kwargs={
                "watched_thread_id": watched_thread.id,
                "secret": watched_thread.secret,
            },
        )
    )
    assert response.status_code == 200

    watched_thread.refresh_from_db()
    assert watched_thread.notifications == ThreadNotifications.DONT_EMAIL


def test_disable_email_notifications_view_returns_404_if_secret_is_invalid(
    watched_thread_factory, user, client, thread
):
    watched_thread = watched_thread_factory(
        user, thread, ThreadNotifications.SEND_EMAIL
    )

    response = client.get(
        reverse(
            "misago:notifications-disable-email",
            kwargs={
                "watched_thread_id": watched_thread.id,
                "secret": "invalid",
            },
        )
    )
    assert response.status_code == 404


def test_disable_email_notifications_view_returns_404_if_watched_thread_is_not_found(
    watched_thread_factory, user, client, thread
):
    watched_thread = watched_thread_factory(
        user, thread, ThreadNotifications.SEND_EMAIL
    )

    response = client.get(
        reverse(
            "misago:notifications-disable-email",
            kwargs={
                "watched_thread_id": watched_thread.id + 1,
                "secret": watched_thread.secret,
            },
        )
    )
    assert response.status_code == 404
