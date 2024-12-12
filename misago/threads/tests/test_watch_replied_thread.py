import pytest
from django.urls import reverse

from ...notifications.models import WatchedThread
from ...notifications.threads import ThreadNotifications
from ..models import ThreadParticipant


@pytest.mark.xfail(reason="Missing implementation")
def test_replied_thread_is_watched_by_user_with_option_enabled(
    notify_on_new_thread_reply_mock, user, user_client, thread
):
    user.watch_replied_threads = ThreadNotifications.SITE_ONLY
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
        send_emails=False,
    )


@pytest.mark.xfail(reason="Missing implementation")
def test_replied_thread_is_not_watched_by_user_with_option_disabled(
    notify_on_new_thread_reply_mock, user, user_client, thread
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


@pytest.mark.xfail(reason="Missing implementation")
def test_replied_private_thread_is_watched_by_user_with_option_enabled(
    notify_on_new_thread_reply_mock, user, user_client, private_thread
):
    user.watch_replied_threads = ThreadNotifications.SITE_ONLY
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
        send_emails=False,
    )


@pytest.mark.xfail(reason="Missing implementation")
def test_replied_private_thread_is_not_watched_by_user_with_option_disabled(
    notify_on_new_thread_reply_mock, user, user_client, private_thread
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
