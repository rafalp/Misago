from django.urls import reverse

from ...test import assert_contains
from ..models import Thread


def test_start_private_thread_view_displays_login_page_to_guests(db, client):
    response = client.get(reverse("misago:start-private-thread"))
    assert_contains(response, "Sign in to start new thread")


def test_start_private_thread_view_displays_error_page_to_users_without_private_threads_permission(
    user, user_client
):
    user.group.can_use_private_threads = False
    user.group.save()

    response = user_client.get(reverse("misago:start-private-thread"))
    assert_contains(
        response,
        "You can&#x27;t use private threads.",
        status_code=403,
    )


def test_start_private_thread_view_displays_error_page_to_users_without_start_threads_permission(
    user, user_client
):
    user.group.can_start_private_threads = False
    user.group.save()

    response = user_client.get(reverse("misago:start-private-thread"))
    assert_contains(
        response,
        "You can&#x27;t start new private threads.",
        status_code=403,
    )


def test_start_private_thread_view_displays_form_page_to_users(user_client):
    response = user_client.get(reverse("misago:start-private-thread"))
    assert_contains(response, "Start new private thread")


def test_start_private_thread_view_posts_new_thread(user_client, other_user):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "users-users": other_user.username,
            "thread-title": "Hello world",
            "thread-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:private-thread", kwargs={"id": thread.id, "slug": thread.slug}
    )


def test_start_private_thread_view_previews_message(user_client, other_user):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "thread-title": "Hello world",
            "thread-post": "How's going?",
            "preview": "true",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(response, "Message preview")
