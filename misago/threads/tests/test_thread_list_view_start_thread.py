from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_start_thread_button_to_guest_with_start_thread_permission(
    db, client
):
    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, reverse("misago:thread-start"))


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_start_thread_button_to_user_with_start_thread_permission(
    user_client,
):
    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, reverse("misago:thread-start"))


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_hides_start_thread_button_from_guest_without_start_thread_permission(
    client, guests_group
):
    CategoryGroupPermission.objects.filter(
        group=guests_group,
        permission=CategoryPermission.START,
    ).delete()

    response = client.get(reverse("misago:thread-list"))
    assert_not_contains(response, reverse("misago:thread-start"))


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_hides_start_thread_button_from_user_without_start_thread_permission(
    user, user_client
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.START,
    ).delete()

    response = user_client.get(reverse("misago:thread-list"))
    assert_not_contains(response, reverse("misago:thread-start"))
