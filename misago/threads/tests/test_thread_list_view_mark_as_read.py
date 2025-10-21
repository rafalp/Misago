from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...readtracker.models import ReadCategory, ReadThread
from ...test import assert_contains


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_mark_as_read_redirects_guests(db, client):
    response = client.post(reverse("misago:thread-list"), {"mark_as_read": "true"})
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_mark_as_read_displays_confirmation_page_to_users(
    user_client,
):
    response = user_client.post(reverse("misago:thread-list"), {"mark_as_read": "true"})
    assert_contains(response, "Mark as read | Threads")
    assert_contains(
        response, "Are you sure you want to mark all threads and categories as read?"
    )


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_mark_as_read_marks_all_categories_as_read(
    user_client, user, default_category, child_category, thread, other_thread
):
    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )
    ReadThread.objects.create(
        user=user,
        category=child_category,
        thread=other_thread,
        read_time=other_thread.last_posted_at,
    )

    response = user_client.post(
        reverse("misago:thread-list"),
        {"mark_as_read": "true", "confirm": "true"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    ReadCategory.objects.get(
        user=user,
        category=default_category,
    )
    ReadCategory.objects.get(
        user=user,
        category=child_category,
    )

    assert not ReadThread.objects.exists()


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_mark_as_read_marks_all_categories_as_read_in_htmx(
    user_client, user, default_category, child_category, thread, other_thread
):
    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )
    ReadThread.objects.create(
        user=user,
        category=child_category,
        thread=other_thread,
        read_time=other_thread.last_posted_at,
    )

    response = user_client.post(
        reverse("misago:thread-list"),
        {"mark_as_read": "true", "confirm": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, other_thread.title)

    ReadCategory.objects.get(
        user=user,
        category=default_category,
    )
    ReadCategory.objects.get(
        user=user,
        category=child_category,
    )

    assert not ReadThread.objects.exists()
