from django.urls import reverse

from ....acl.test import patch_user_acl
from ....notifications.enums import ThreadNotifications
from ....notifications.models import WatchedThread


def test_thread_watch_api_creates_watched_thread_with_notifications_disabled(
    user, thread, user_client
):
    response = user_client.post(
        reverse("misago:apiv2:thread-watch", kwargs={"thread_id": thread.id}),
        json={"notifications": ThreadNotifications.NONE.value},
    )

    assert response.status_code == 200
    assert response.json() == {"notifications": ThreadNotifications.NONE.value}

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.category_id == thread.category_id
    assert watched_thread.notifications == ThreadNotifications.NONE


def test_thread_watch_api_creates_watched_thread_with_notifications(
    user, thread, user_client
):
    response = user_client.post(
        reverse("misago:apiv2:thread-watch", kwargs={"thread_id": thread.id}),
        json={"notifications": ThreadNotifications.DONT_EMAIL.value},
    )

    assert response.status_code == 200
    assert response.json() == {"notifications": ThreadNotifications.DONT_EMAIL.value}

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.category_id == thread.category_id
    assert watched_thread.notifications == ThreadNotifications.DONT_EMAIL


def test_thread_watch_api_creates_watched_thread_with_email_notifications(
    user, thread, user_client
):
    response = user_client.post(
        reverse("misago:apiv2:thread-watch", kwargs={"thread_id": thread.id}),
        json={"notifications": ThreadNotifications.SEND_EMAIL.value},
    )

    assert response.status_code == 200
    assert response.json() == {"notifications": ThreadNotifications.SEND_EMAIL.value}

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.category_id == thread.category_id
    assert watched_thread.notifications == ThreadNotifications.SEND_EMAIL


def test_thread_watch_api_updates_watched_thread_with_email_notifications(
    user, thread, user_client, django_assert_num_queries
):
    existing_watched_thread = WatchedThread.objects.create(
        user=user,
        category_id=thread.category_id,
        thread=thread,
        notifications=ThreadNotifications.NONE,
    )

    with django_assert_num_queries(25):
        response = user_client.post(
            reverse("misago:apiv2:thread-watch", kwargs={"thread_id": thread.id}),
            json={"notifications": ThreadNotifications.SEND_EMAIL.value},
        )

    assert response.status_code == 200
    assert response.json() == {"notifications": ThreadNotifications.SEND_EMAIL.value}

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.id == existing_watched_thread.id
    assert watched_thread.notifications == ThreadNotifications.SEND_EMAIL


def test_thread_watch_api_skips_update_if_notifications_are_not_changed(
    user, thread, user_client, django_assert_num_queries
):
    existing_watched_thread = WatchedThread.objects.create(
        user=user,
        category_id=thread.category_id,
        thread=thread,
        notifications=ThreadNotifications.SEND_EMAIL,
    )

    with django_assert_num_queries(24):
        response = user_client.post(
            reverse("misago:apiv2:thread-watch", kwargs={"thread_id": thread.id}),
            json={"notifications": ThreadNotifications.SEND_EMAIL.value},
        )

    assert response.status_code == 200
    assert response.json() == {"notifications": ThreadNotifications.SEND_EMAIL.value}

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.id == existing_watched_thread.id
    assert watched_thread.notifications == ThreadNotifications.SEND_EMAIL


def test_thread_watch_api_returns_404_error_if_thread_doesnt_exist(user, user_client):
    response = user_client.post(
        reverse("misago:apiv2:thread-watch", kwargs={"thread_id": 404}),
        json={"notifications": ThreadNotifications.SEND_EMAIL.value},
    )

    assert response.status_code == 404
    assert WatchedThread.objects.count() == 0


def test_thread_watch_api_returns_404_error_if_thread_is_not_accessible(
    user, other_user_hidden_thread, user_client
):
    response = user_client.post(
        reverse(
            "misago:apiv2:thread-watch",
            kwargs={"thread_id": other_user_hidden_thread.id},
        ),
        json={"notifications": ThreadNotifications.SEND_EMAIL.value},
    )

    assert response.status_code == 404
    assert WatchedThread.objects.count() == 0


def test_thread_watch_api_returns_400_error_if_notifications_are_not_provided(
    user, thread, user_client
):
    response = user_client.post(
        reverse("misago:apiv2:thread-watch", kwargs={"thread_id": thread.id}), json={}
    )

    assert response.status_code == 400
    assert response.json() == {"notifications": ["This field is required."]}

    assert WatchedThread.objects.count() == 0


def test_thread_watch_api_returns_400_error_if_notifications_are_invalid(
    user, thread, user_client
):
    response = user_client.post(
        reverse("misago:apiv2:thread-watch", kwargs={"thread_id": thread.id}),
        json={"notifications": 42},
    )

    assert response.status_code == 400
    assert response.json() == {"notifications": ['"42" is not a valid choice.']}

    assert WatchedThread.objects.count() == 0


def test_thread_watch_api_returns_403_error_if_client_is_no_authenticated(
    thread, client
):
    response = client.post(
        reverse("misago:apiv2:thread-watch", kwargs={"thread_id": thread.id}),
        json={"notifications": ThreadNotifications.SEND_EMAIL.value},
    )

    assert response.status_code == 403
    assert WatchedThread.objects.count() == 0


def test_thread_watch_api_returns_404_error_if_thread_is_private(
    user, private_thread, user_client
):
    response = user_client.post(
        reverse("misago:apiv2:thread-watch", kwargs={"thread_id": private_thread.id}),
        json={"notifications": ThreadNotifications.SEND_EMAIL.value},
    )

    assert response.status_code == 404
    assert WatchedThread.objects.count() == 0


def test_private_thread_watch_api_creates_watched_thread_with_notifications(
    user, private_thread, user_client
):
    private_thread.threadparticipant_set.create(user=user)

    response = user_client.post(
        reverse(
            "misago:apiv2:private-thread-watch", kwargs={"thread_id": private_thread.id}
        ),
        json={"notifications": ThreadNotifications.DONT_EMAIL.value},
    )

    assert response.status_code == 200
    assert response.json() == {"notifications": ThreadNotifications.DONT_EMAIL.value}

    watched_thread = WatchedThread.objects.get(user=user, thread=private_thread)
    assert watched_thread.category_id == private_thread.category_id
    assert watched_thread.notifications == ThreadNotifications.DONT_EMAIL


def test_private_thread_watch_api_returns_404_error_if_user_has_no_access_to_thread(
    user, private_thread, user_client
):
    response = user_client.post(
        reverse(
            "misago:apiv2:private-thread-watch", kwargs={"thread_id": private_thread.id}
        ),
        json={"notifications": ThreadNotifications.DONT_EMAIL.value},
    )

    assert response.status_code == 404
    assert WatchedThread.objects.count() == 0


def test_private_thread_watch_api_returns_404_error_if_thread_is_not_private_thread(
    user, thread, user_client
):
    response = user_client.post(
        reverse("misago:apiv2:private-thread-watch", kwargs={"thread_id": thread.id}),
        json={"notifications": ThreadNotifications.DONT_EMAIL.value},
    )

    assert response.status_code == 404
    assert WatchedThread.objects.count() == 0


def test_private_thread_watch_api_returns_403_error_if_client_is_no_authenticated(
    user, private_thread, client
):
    private_thread.threadparticipant_set.create(user=user)

    response = client.post(
        reverse(
            "misago:apiv2:private-thread-watch", kwargs={"thread_id": private_thread.id}
        ),
        json={"notifications": ThreadNotifications.DONT_EMAIL.value},
    )

    assert response.status_code == 403
    assert WatchedThread.objects.count() == 0


@patch_user_acl({"can_use_private_threads": False})
def test_private_thread_watch_api_returns_403_if_user_cant_use_private_threads(
    user, private_thread, user_client
):
    private_thread.threadparticipant_set.create(user=user)

    response = user_client.post(
        reverse(
            "misago:apiv2:private-thread-watch", kwargs={"thread_id": private_thread.id}
        ),
        json={"notifications": ThreadNotifications.DONT_EMAIL.value},
    )

    assert response.status_code == 403
    assert WatchedThread.objects.count() == 0
