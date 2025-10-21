from ...readtracker.models import ReadCategory, ReadThread
from ...test import assert_contains


def test_category_thread_list_view_mark_as_read_redirects_guests(
    default_category, client
):
    response = client.post(
        default_category.get_absolute_url(), {"mark_as_read": "true"}
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()


def test_category_thread_list_view_mark_as_read_displays_confirmation_page_to_users(
    default_category, user_client
):
    response = user_client.post(
        default_category.get_absolute_url(), {"mark_as_read": "true"}
    )
    assert_contains(response, f"Mark as read | {default_category}")
    assert_contains(
        response, "Are you sure you want to mark all threads in this category as read?"
    )


def test_category_thread_list_view_mark_as_read_marks_category_as_read(
    default_category, user_client, user, thread
):
    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )

    response = user_client.post(
        default_category.get_absolute_url(),
        {"mark_as_read": "true", "confirm": "true"},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    ReadCategory.objects.get(
        user=user,
        category=default_category,
    )

    assert not ReadThread.objects.exists()


def test_category_thread_list_view_mark_as_read_marks_category_as_read_in_htmx(
    default_category, user_client, user, thread
):
    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )

    response = user_client.post(
        default_category.get_absolute_url(),
        {"mark_as_read": "true", "confirm": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)

    ReadCategory.objects.get(
        user=user,
        category=default_category,
    )

    assert not ReadThread.objects.exists()


def test_category_thread_list_view_mark_as_read_marks_child_category_as_read(
    default_category, child_category, user_client, user, thread
):
    ReadThread.objects.create(
        user=user,
        category=child_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )

    response = user_client.post(
        default_category.get_absolute_url(),
        {"mark_as_read": "true", "confirm": "true"},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    ReadCategory.objects.get(
        user=user,
        category=default_category,
    )
    ReadCategory.objects.get(
        user=user,
        category=child_category,
    )

    assert not ReadThread.objects.exists()


def test_category_thread_list_view_mark_as_read_doesnt_mark_child_category_as_read_if_listing_is_disabled(
    default_category, child_category, user_client, user, thread, other_thread
):
    default_category.list_children_threads = False
    default_category.save()

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
        default_category.get_absolute_url(), {"mark_as_read": "true", "confirm": "true"}
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    ReadCategory.objects.get(
        user=user,
        category=default_category,
    )

    assert not ReadCategory.objects.filter(user=user, category=child_category).exists()
    assert ReadThread.objects.filter(category=child_category).exists()
