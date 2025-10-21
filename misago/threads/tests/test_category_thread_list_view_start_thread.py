from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains


def test_category_thread_list_view_shows_start_thread_button_to_guest_with_start_thread_permission(
    client, default_category
):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(
        response,
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_category_thread_list_view_shows_start_thread_button_to_user_with_start_thread_permission(
    user_client, default_category
):
    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(
        response,
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_category_thread_list_view_doesnt_show_start_thread_button_to_guest_without_start_thread_permission(
    client, guests_group, default_category
):
    CategoryGroupPermission.objects.filter(
        group=guests_group,
        permission=CategoryPermission.START,
    ).delete()

    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_not_contains(
        response,
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_category_thread_list_view_doesnt_show_start_thread_button_to_user_without_start_thread_permission(
    user, user_client, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.START,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_not_contains(response, reverse("misago:thread-start"))


def test_category_thread_list_view_hides_start_thread_button_from_user_without_permission_in_closed_category(
    user_client, default_category
):
    default_category.is_closed = True
    default_category.save()

    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_not_contains(
        response,
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_category_thread_list_view_shows_start_thread_button_to_user_with_permission_in_closed_category(
    user, user_client, default_category, members_group, moderators_group
):
    default_category.is_closed = True
    default_category.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(
        response,
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )
