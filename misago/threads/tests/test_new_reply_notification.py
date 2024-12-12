import pytest
from django.urls import reverse

from ..models import ThreadParticipant


@pytest.mark.xfail(reason="Missing implementation")
def test_notify_about_new_reply_task_is_triggered_by_new_thread_reply(
    notify_on_new_thread_reply_mock, user_client, thread
):
    response = user_client.post(
        reverse("misago:api:thread-post-list", kwargs={"thread_pk": thread.pk}),
        data={
            "post": "Lorem ipsum dolor met",
        },
    )

    assert response.status_code == 200

    data = response.json()
    notify_on_new_thread_reply_mock.delay.assert_called_once_with(data["id"])


@pytest.mark.xfail(reason="Missing implementation")
def test_notify_about_new_reply_task_is_triggered_by_new_private_thread_reply(
    notify_on_new_thread_reply_mock,
    user,
    user_client,
    private_thread,
):
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

    data = response.json()
    notify_on_new_thread_reply_mock.delay.assert_called_once_with(data["id"])


@pytest.mark.xfail(reason="Missing implementation")
def test_notify_about_new_reply_task_is_not_triggered_on_new_thread_start(
    notify_on_new_thread_reply_mock, user_client, default_category
):
    response = user_client.post(
        reverse("misago:api:thread-list"),
        data={
            "category": default_category.pk,
            "title": "Test thread",
            "post": "Lorem ipsum dolor met",
        },
    )

    assert response.status_code == 200

    notify_on_new_thread_reply_mock.delay.assert_not_called()


@pytest.mark.xfail(reason="Missing implementation")
def test_notify_about_new_reply_task_is_not_triggered_on_new_private_thread_start(
    notify_on_new_private_thread_mock,
    notify_on_new_thread_reply_mock,
    other_user,
    user_client,
):
    response = user_client.post(
        reverse("misago:api:private-thread-list"),
        data={
            "to": [other_user.username],
            "title": "Test thread",
            "post": "Lorem ipsum dolor met",
        },
    )

    assert response.status_code == 200

    notify_on_new_thread_reply_mock.delay.assert_not_called()


def test_notify_about_new_reply_task_is_not_triggered_on_thread_reply_edit(
    notify_on_new_thread_reply_mock,
    user_client,
    thread,
    user_reply,
):
    response = user_client.put(
        reverse(
            "misago:api:thread-post-detail",
            kwargs={"thread_pk": thread.id, "pk": user_reply.id},
        ),
        json={
            "post": "Edited reply",
        },
    )

    assert response.status_code == 200

    notify_on_new_thread_reply_mock.delay.assert_not_called()


def test_notify_about_new_reply_task_is_not_triggered_on_private_thread_reply_edit(
    notify_on_new_thread_reply_mock,
    user,
    user_client,
    private_thread,
    private_thread_user_reply,
):
    ThreadParticipant.objects.create(thread=private_thread, user=user)

    response = user_client.put(
        reverse(
            "misago:api:private-thread-post-detail",
            kwargs={"thread_pk": private_thread.id, "pk": private_thread_user_reply.id},
        ),
        json={
            "post": "Edited reply",
        },
    )

    assert response.status_code == 200

    notify_on_new_thread_reply_mock.delay.assert_not_called()
