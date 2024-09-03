from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...readtracker.models import ReadCategory, ReadThread
from ...test import assert_contains


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_mark_as_read_redirects_guests(db, client):
    response = client.post(reverse("misago:threads"), {"mark_as_read": "true"})
    assert response.status_code == 302
    assert response["location"] == reverse("misago:threads")


def test_category_threads_list_mark_as_read_redirects_guests(default_category, client):
    response = client.post(
        default_category.get_absolute_url(), {"mark_as_read": "true"}
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_mark_as_read_displays_confirmation_page_to_users(
    user_client,
):
    response = user_client.post(reverse("misago:threads"), {"mark_as_read": "true"})
    assert_contains(response, "Mark as read | Threads")
    assert_contains(
        response, "Are you sure you want to mark all threads and categories as read?"
    )


def test_category_threads_list_mark_as_read_displays_confirmation_page_to_users(
    default_category, user_client
):
    response = user_client.post(
        default_category.get_absolute_url(), {"mark_as_read": "true"}
    )
    assert_contains(response, f"Mark as read | {default_category}")
    assert_contains(
        response, "Are you sure you want to mark all threads in this category as read?"
    )


def test_private_threads_list_mark_as_read_displays_confirmation_page_to_users(
    user_client,
):
    response = user_client.post(
        reverse("misago:private-threads"), {"mark_as_read": "true"}
    )
    assert_contains(response, f"Mark as read | Private threads")
    assert_contains(
        response, "Are you sure you want to mark all private threads as read?"
    )


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_mark_as_read_marks_all_categories_as_read(
    user_client, user, default_category, child_category, thread, other_thread
):
    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_post_on,
    )
    ReadThread.objects.create(
        user=user,
        category=child_category,
        thread=other_thread,
        read_time=other_thread.last_post_on,
    )

    response = user_client.post(
        reverse("misago:threads"),
        {"mark_as_read": "true", "confirm": "true"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:threads")

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
def test_site_threads_list_mark_as_read_marks_all_categories_as_read_in_htmx(
    user_client, user, default_category, child_category, thread, other_thread
):
    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_post_on,
    )
    ReadThread.objects.create(
        user=user,
        category=child_category,
        thread=other_thread,
        read_time=other_thread.last_post_on,
    )

    response = user_client.post(
        reverse("misago:threads"),
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


def test_category_threads_list_mark_as_read_marks_category_as_read(
    default_category, user_client, user, thread
):
    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_post_on,
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


def test_category_threads_list_mark_as_read_marks_category_as_read_in_htmx(
    default_category, user_client, user, thread
):
    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_post_on,
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


def test_category_threads_list_mark_as_read_marks_child_category_as_read(
    default_category, child_category, user_client, user, thread
):
    ReadThread.objects.create(
        user=user,
        category=child_category,
        thread=thread,
        read_time=thread.last_post_on,
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


def test_category_threads_list_mark_as_read_doesnt_mark_child_category_as_read_if_listing_is_disabled(
    default_category, child_category, user_client, user, thread, other_thread
):
    default_category.list_children_threads = False
    default_category.save()

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_post_on,
    )
    ReadThread.objects.create(
        user=user,
        category=child_category,
        thread=other_thread,
        read_time=other_thread.last_post_on,
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


def test_private_threads_list_mark_as_read_marks_private_threads_as_read(
    user_client, user, private_threads_category, user_private_thread
):
    ReadThread.objects.create(
        user=user,
        category=private_threads_category,
        thread=user_private_thread,
        read_time=user_private_thread.last_post_on,
    )

    response = user_client.post(
        reverse("misago:private-threads"), {"mark_as_read": "true", "confirm": "true"}
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:private-threads")

    ReadCategory.objects.get(
        user=user,
        category=private_threads_category,
    )

    assert not ReadThread.objects.exists()


def test_private_threads_list_mark_as_read_marks_private_threads_as_read_in_htmx(
    user_client, user, private_threads_category, user_private_thread
):
    ReadThread.objects.create(
        user=user,
        category=private_threads_category,
        thread=user_private_thread,
        read_time=user_private_thread.last_post_on,
    )

    response = user_client.post(
        reverse("misago:private-threads"),
        {"mark_as_read": "true", "confirm": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_private_thread.title)

    ReadCategory.objects.get(
        user=user,
        category=private_threads_category,
    )

    assert not ReadThread.objects.exists()


def test_private_threads_list_mark_as_read_clears_user_unread_private_threads_count(
    user_client, user
):
    user.unread_private_threads = 120
    user.save()

    response = user_client.post(
        reverse("misago:private-threads"), {"mark_as_read": "true", "confirm": "true"}
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:private-threads")

    user.refresh_from_db()
    assert user.unread_private_threads == 0
