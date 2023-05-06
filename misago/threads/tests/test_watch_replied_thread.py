from django.urls import reverse

from ...notifications.enums import ThreadNotifications
from ...notifications.models import WatchedThread
from ..models import ThreadParticipant


def test_replied_thread_is_watched_by_user_with_option_enabled(
    user, user_client, thread
):
    user.watch_replied_threads = ThreadNotifications.DONT_EMAIL
    user.save()

    response = user_client.post(
        reverse("misago:api:thread-post-list", kwargs={"thread_pk": thread.pk}),
        data={
            "post": "Lorem ipsum dolor met",
        },
    )

    assert response.status_code == 200

    WatchedThread.objects.get(
        user=user,
        category_id=thread.category_id,
        thread=thread,
        notifications=ThreadNotifications.DONT_EMAIL,
    )


def test_replied_thread_is_not_watched_by_user_with_option_disabled(
    user, user_client, thread
):
    user.watch_replied_threads = ThreadNotifications.NONE
    user.save()

    response = user_client.post(
        reverse("misago:api:thread-post-list", kwargs={"thread_pk": thread.pk}),
        data={
            "post": "Lorem ipsum dolor met",
        },
    )

    assert response.status_code == 200
    assert not WatchedThread.objects.exists()


def test_replied_private_thread_is_watched_by_user_with_option_enabled(
    user, user_client, private_thread
):
    user.watch_replied_threads = ThreadNotifications.DONT_EMAIL
    user.save()

    ThreadParticipant.objects.create(thread=private_thread, user=user)

    response = user_client.post(
        reverse(
            "misago:api:private-thread-post-list",
            kwargs={"thread_pk": private_thread.pk},
        ),
        data={
            "post": "Lorem ipsum dolor met",
        },
    )

    assert response.status_code == 200

    WatchedThread.objects.get(
        user=user,
        category_id=private_thread.category_id,
        thread=private_thread,
        notifications=ThreadNotifications.DONT_EMAIL,
    )


def test_replied_private_thread_is_not_watched_by_user_with_option_disabled(
    user, user_client, private_thread
):
    user.watch_replied_threads = ThreadNotifications.NONE
    user.save()

    ThreadParticipant.objects.create(thread=private_thread, user=user)

    response = user_client.post(
        reverse(
            "misago:api:private-thread-post-list",
            kwargs={"thread_pk": private_thread.pk},
        ),
        data={
            "post": "Lorem ipsum dolor met",
        },
    )

    assert response.status_code == 200
    assert not WatchedThread.objects.exists()
