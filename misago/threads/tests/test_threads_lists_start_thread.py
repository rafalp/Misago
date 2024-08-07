from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_start_thread_button_to_guest_with_permission(
    guests_group, client, default_category
):
    response = client.get(reverse("misago:threads"))
    assert_contains(response, reverse("misago:start-thread"))


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_start_thread_button_to_user_with_permission(user_client):
    response = user_client.get(reverse("misago:threads"))
    assert_contains(response, reverse("misago:start-thread"))


def test_category_threads_list_displays_start_thread_button_to_guest_with_permission(
    guests_group, client, default_category
):
    response = client.get(
        reverse(
            "misago:category",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, reverse("misago:start-thread"))


def test_category_threads_list_displays_start_thread_button_to_user_with_permission(
    user_client, default_category
):
    response = user_client.get(
        reverse(
            "misago:category",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, reverse("misago:start-thread"))


def test_private_threads_list_displays_start_thread_button_to_user_with_permission(
    user_client,
):
    response = user_client.get(reverse("misago:private-threads"))
    assert_contains(response, reverse("misago:start-private-thread"))


@override_dynamic_settings(index_view="categories")
def test_threads_list_hides_start_thread_button_from_guest_without_permission(
    client, guests_group
):
    CategoryGroupPermission.objects.filter(
        group=guests_group,
        permission=CategoryPermission.START,
    ).delete()

    response = client.get(reverse("misago:threads"))
    assert_not_contains(response, reverse("misago:start-thread"))


@override_dynamic_settings(index_view="categories")
def test_threads_list_hides_start_thread_button_from_user_without_permission(
    user, user_client
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.START,
    ).delete()

    response = user_client.get(reverse("misago:threads"))
    assert_not_contains(response, reverse("misago:start-thread"))


def test_category_threads_list_hides_start_thread_button_from_guest_without_permission(
    client, guests_group, default_category
):
    CategoryGroupPermission.objects.filter(
        group=guests_group,
        permission=CategoryPermission.START,
    ).delete()

    response = client.get(
        reverse(
            "misago:category",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_not_contains(response, reverse("misago:start-thread"))


def test_category_threads_list_hides_start_thread_button_from_user_without_permission(
    user, user_client, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.START,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:category",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_not_contains(response, reverse("misago:start-thread"))


def test_private_threads_list_hides_start_thread_button_from_user_without_permission(
    user, user_client
):
    user.group.can_start_private_threads = False
    user.group.save()

    response = user_client.get(reverse("misago:private-threads"))
    assert_not_contains(response, reverse("misago:start-private-thread"))


def test_closed_category_threads_list_hides_start_thread_button_from_user_without_permission(
    user_client, default_category
):
    default_category.is_closed = True
    default_category.save()

    response = user_client.get(
        reverse(
            "misago:category",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_not_contains(response, reverse("misago:start-thread"))


def test_closed_category_threads_list_shows_start_thread_button_to_user_with_permission(
    user, user_client, default_category, members_group, moderators_group
):
    default_category.is_closed = True
    default_category.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:category",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, reverse("misago:start-thread"))
