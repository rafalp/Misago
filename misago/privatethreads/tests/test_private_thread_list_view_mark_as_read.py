from django.urls import reverse

from ...readtracker.models import ReadCategory, ReadThread
from ...test import assert_contains


def test_private_thread_list_view_mark_as_read_displays_confirmation_page_to_users(
    user_client,
):
    response = user_client.post(
        reverse("misago:private-thread-list"), {"mark_as_read": "true"}
    )
    assert_contains(response, f"Mark as read | Private threads")
    assert_contains(
        response, "Are you sure you want to mark all private threads as read?"
    )


def test_private_thread_list_view_mark_as_read_marks_private_threads_as_read(
    user_client, user, private_threads_category, user_private_thread
):
    ReadThread.objects.create(
        user=user,
        category=private_threads_category,
        thread=user_private_thread,
        read_time=user_private_thread.last_posted_at,
    )

    response = user_client.post(
        reverse("misago:private-thread-list"),
        {"mark_as_read": "true", "confirm": "true"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:private-thread-list")

    ReadCategory.objects.get(
        user=user,
        category=private_threads_category,
    )

    assert not ReadThread.objects.exists()


def test_private_thread_list_view_mark_as_read_marks_private_threads_as_read_in_htmx(
    user_client, user, private_threads_category, user_private_thread
):
    ReadThread.objects.create(
        user=user,
        category=private_threads_category,
        thread=user_private_thread,
        read_time=user_private_thread.last_posted_at,
    )

    response = user_client.post(
        reverse("misago:private-thread-list"),
        {"mark_as_read": "true", "confirm": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_private_thread.title)

    ReadCategory.objects.get(
        user=user,
        category=private_threads_category,
    )

    assert not ReadThread.objects.exists()


def test_private_thread_list_view_mark_as_read_clears_user_unread_private_threads_count(
    user_client, user
):
    user.unread_private_threads = 120
    user.save()

    response = user_client.post(
        reverse("misago:private-thread-list"),
        {"mark_as_read": "true", "confirm": "true"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:private-thread-list")

    user.refresh_from_db()
    assert user.unread_private_threads == 0
