from django.urls import reverse

from ....notifications.models import Notification


def test_notifications_api_returns_403_error_if_client_is_no_authenticated(db, client):
    response = client.get(reverse("misago:apiv2:notifications"))
    assert response.status_code == 403


def test_notifications_api_returns_empty_list_if_user_has_no_notifications(user_client):
    response = user_client.get(reverse("misago:apiv2:notifications"))
    assert response.status_code == 200
    assert response.json() == {
        "results": [],
        "hasNext": False,
        "hasPrevious": False,
    }


def test_notifications_api_returns_list_with_all_user_notifications(user, user_client):
    read_notification = Notification.objects.create(
        user=user, verb="tested", is_read=True
    )
    notification = Notification.objects.create(user=user, verb="tested", is_read=False)

    response = user_client.get(reverse("misago:apiv2:notifications"))
    assert response.status_code == 200

    response_json = response.json()
    assert [result["id"] for result in response_json["results"]] == [
        notification.id,
        read_notification.id,
    ]
    assert not response_json["hasNext"]
    assert not response_json["hasPrevious"]


def test_notifications_api_returns_list_with_read_user_notifications(user, user_client):
    read_notification = Notification.objects.create(
        user=user, verb="tested", is_read=True
    )
    Notification.objects.create(user=user, verb="tested", is_read=False)

    response = user_client.get(reverse("misago:apiv2:notifications") + "?filter=read")
    assert response.status_code == 200

    response_json = response.json()
    assert [result["id"] for result in response_json["results"]] == [
        read_notification.id
    ]
    assert not response_json["hasNext"]
    assert not response_json["hasPrevious"]


def test_notifications_api_returns_list_with_unread_user_notifications(
    user, user_client
):
    Notification.objects.create(user=user, verb="tested", is_read=True)
    notification = Notification.objects.create(user=user, verb="tested", is_read=False)

    response = user_client.get(reverse("misago:apiv2:notifications") + "?filter=unread")
    assert response.status_code == 200

    response_json = response.json()
    assert [result["id"] for result in response_json["results"]] == [notification.id]
    assert not response_json["hasNext"]
    assert not response_json["hasPrevious"]


def test_notifications_api_clears_user_unread_notifications_count_if_unread_list_is_empty(
    user, user_client
):
    user.unread_notifications = 10
    user.save()

    response = user_client.get(reverse("misago:apiv2:notifications") + "?filter=unread")
    assert response.status_code == 200

    response_json = response.json()
    assert not response_json["results"]
    assert not response_json["hasNext"]
    assert not response_json["hasPrevious"]

    user.refresh_from_db()
    assert user.unread_notifications == 0


def test_notifications_api_excludes_other_users_notifications(
    user, other_user, user_client
):
    Notification.objects.create(user=other_user, verb="tested", is_read=True)
    notification = Notification.objects.create(user=user, verb="tested", is_read=False)

    response = user_client.get(reverse("misago:apiv2:notifications"))
    assert response.status_code == 200

    response_json = response.json()
    assert [result["id"] for result in response_json["results"]] == [notification.id]
    assert not response_json["hasNext"]
    assert not response_json["hasPrevious"]


def test_notifications_api_supports_limiting_results_count(user, user_client):
    Notification.objects.create(user=user, verb="tested", is_read=False)
    Notification.objects.create(user=user, verb="tested", is_read=False)
    Notification.objects.create(user=user, verb="tested", is_read=False)

    response = user_client.get(reverse("misago:apiv2:notifications") + "?limit=2")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json["results"]) == 2
    assert response_json["hasNext"]
    assert not response_json["hasPrevious"]


def test_notifications_api_returns_400_error_if_too_many_results_are_requested(
    user, user_client
):
    Notification.objects.create(user=user, verb="tested", is_read=False)
    Notification.objects.create(user=user, verb="tested", is_read=False)
    Notification.objects.create(user=user, verb="tested", is_read=False)

    response = user_client.get(reverse("misago:apiv2:notifications") + "?limit=2000")
    assert response.status_code == 400
