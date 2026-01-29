from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...readtracker.models import ReadCategory, ReadThread
from ...test import assert_contains


@override_dynamic_settings(index_view="threads")
def test_categories_view_mark_as_read_displays_categories_to_anonymous_users(
    default_category, client
):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.save()

    response = client.post(reverse("misago:categories"), {"mark_as_read": "true"})
    assert_contains(response, default_category.description)


@override_dynamic_settings(index_view="threads")
def test_categories_view_mark_as_read_displays_confirmation_page_to_users(user_client):
    response = user_client.post(reverse("misago:categories"), {"mark_as_read": "true"})
    assert_contains(response, "Mark as read | Categories")
    assert_contains(response, "Are you sure you want to mark all categories as read?")


@override_dynamic_settings(index_view="threads")
def test_categories_view_mark_as_read_marks_categories_read(
    user_client, default_category, user, thread
):
    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )

    response = user_client.post(
        reverse("misago:categories"), {"mark_as_read": "true", "confirm": "true"}
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:categories")

    ReadCategory.objects.get(
        user=user,
        category=default_category,
    )

    assert not ReadThread.objects.exists()


@override_dynamic_settings(index_view="threads")
def test_categories_view_mark_as_read_marks_categories_read_in_htmx(
    user_client, default_category, user, thread
):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.save()

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )

    response = user_client.post(
        reverse("misago:categories"),
        {"mark_as_read": "true", "confirm": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, default_category.description)

    ReadCategory.objects.get(
        user=user,
        category=default_category,
    )

    assert not ReadThread.objects.exists()
