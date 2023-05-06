from django.urls import reverse

from ...notifications.enums import ThreadNotifications
from ...notifications.models import WatchedThread


def test_started_thread_is_watched_by_user_with_option_enabled(
    user, user_client, default_category
):
    user.watch_started_threads = ThreadNotifications.DONT_EMAIL
    user.save()

    response = user_client.post(
        reverse("misago:api:thread-list"),
        data={
            "category": default_category.pk,
            "title": "Test thread",
            "post": "Lorem ipsum dolor met",
        },
    )

    assert response.status_code == 200

    data = response.json()

    WatchedThread.objects.get(
        user=user,
        category=default_category,
        thread_id=data["id"],
        notifications=ThreadNotifications.DONT_EMAIL,
    )


def test_started_thread_is_not_watched_by_user_with_option_disabled(
    user, user_client, default_category
):
    user.watch_started_threads = ThreadNotifications.NONE
    user.save()

    response = user_client.post(
        reverse("misago:api:thread-list"),
        data={
            "category": default_category.pk,
            "title": "Test thread",
            "post": "Lorem ipsum dolor met",
        },
    )

    assert response.status_code == 200
    assert not WatchedThread.objects.exists()


def test_started_private_thread_is_watched_by_user_with_option_enabled(
    notify_on_new_private_thread_mock,
    user,
    user_client,
    other_user,
    private_threads_category,
):
    user.watch_started_threads = ThreadNotifications.DONT_EMAIL
    user.save()

    response = user_client.post(
        reverse("misago:api:private-thread-list"),
        data={
            "to": [other_user.username],
            "title": "Test thread",
            "post": "Lorem ipsum dolor met",
        },
    )

    assert response.status_code == 200

    data = response.json()

    WatchedThread.objects.get(
        user=user,
        category=private_threads_category,
        thread_id=data["id"],
        notifications=ThreadNotifications.DONT_EMAIL,
    )


def test_started_private_thread_is_not_watched_by_user_with_option_disabled(
    notify_on_new_private_thread_mock, user, user_client, other_user
):
    user.watch_started_threads = ThreadNotifications.NONE
    user.save()

    response = user_client.post(
        reverse("misago:api:private-thread-list"),
        data={
            "to": [other_user.username],
            "title": "Test thread",
            "post": "Lorem ipsum dolor met",
        },
    )

    assert response.status_code == 200
    assert not WatchedThread.objects.exists()
