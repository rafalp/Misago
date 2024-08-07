from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains


def test_start_thread_view_displays_login_page_to_guests(client, default_category):
    response = client.get(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, "Sign in to start new thread")


def test_start_thread_view_displays_error_page_to_users_without_see_category_permission(
    user_client, user, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.SEE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert response.status_code == 404


def test_start_thread_view_displays_error_page_to_users_without_browse_category_permission(
    user_client, user, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t browse the contents of this category.",
        status_code=403,
    )


def test_start_thread_view_displays_error_page_to_users_without_start_threads_permission(
    user_client, user, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.START,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t start new threads in this category.",
        status_code=403,
    )


def test_start_thread_view_displays_form_page_to_users(user_client, default_category):
    response = user_client.get(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, "Start new thread")
