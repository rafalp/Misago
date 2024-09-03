from datetime import timedelta

from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.enums import CategoryPermission
from ...test import assert_contains, assert_not_contains
from ...testutils import (
    grant_category_group_permissions,
    remove_category_group_permissions,
)
from ..models import Category


@override_dynamic_settings(index_view="threads")
def test_categories_view_displays_default_category_for_guest(default_category, client):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.save()

    response = client.get(reverse("misago:categories"))
    assert_contains(response, default_category.description)


@override_dynamic_settings(index_view="threads")
def test_categories_view_displays_default_category_for_user(
    default_category, user_client
):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.save()

    response = user_client.get(reverse("misago:categories"))
    assert_contains(response, default_category.description)


@override_dynamic_settings(index_view="threads")
def test_categories_view_displays_for_guest_in_htmx(default_category, client):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.save()

    response = client.get(
        reverse("misago:categories"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, default_category.description)


@override_dynamic_settings(index_view="threads")
def test_categories_view_displays_for_user_in_htmx(default_category, user_client):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.save()

    response = user_client.get(
        reverse("misago:categories"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, default_category.description)


@override_dynamic_settings(index_view="threads")
def test_categories_view_excludes_default_category_for_guest_without_permission(
    default_category, guests_group, client
):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.save()

    remove_category_group_permissions(default_category, guests_group)

    response = client.get(reverse("misago:categories"))
    assert_not_contains(response, default_category.description)


@override_dynamic_settings(index_view="threads")
def test_categories_view_excludes_default_category_for_user_without_permission(
    default_category, user, user_client
):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.save()

    remove_category_group_permissions(default_category, user.group)

    response = user_client.get(reverse("misago:categories"))
    assert_not_contains(response, default_category.description)


@override_dynamic_settings(index_view="threads")
def test_categories_view_displays_child_category_for_user_with_permission(
    default_category, user, user_client
):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.save()

    child_category = Category(
        name="Child Category",
        slug="child-category",
        description="CHILD-CATEGORY-DESCRIPTION",
    )

    child_category.insert_at(default_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
    )

    response = user_client.get(reverse("misago:categories"))
    assert_contains(response, default_category.description)
    assert_contains(response, child_category.description)


@override_dynamic_settings(index_view="threads")
def test_categories_view_displays_child_category_for_category_with_delay_browse_check(
    default_category, user, user_client
):
    default_category.delay_browse_check = True
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.save()

    child_category = Category(
        name="Child Category",
        slug="child-category",
        description="CHILD-CATEGORY-DESCRIPTION",
    )

    child_category.insert_at(default_category, position="last-child", save=True)

    remove_category_group_permissions(default_category, user.group)

    grant_category_group_permissions(
        default_category,
        user.group,
        CategoryPermission.SEE,
    )
    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
    )

    response = user_client.get(reverse("misago:categories"))
    assert_contains(response, default_category.description)
    assert_contains(response, child_category.description)


@override_dynamic_settings(index_view="threads")
def test_categories_view_excludes_child_category_for_user_without_permission(
    default_category, user_client
):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.save()

    child_category = Category(
        name="Child Category",
        slug="child-category",
        description="CHILD-CATEGORY-DESCRIPTION",
    )

    child_category.insert_at(default_category, position="last-child", save=True)

    response = user_client.get(reverse("misago:categories"))
    assert_contains(response, default_category.description)
    assert_not_contains(response, child_category.description)


@override_dynamic_settings(index_view="threads")
def test_categories_view_displays_category_user_thread(
    default_category, user_client, user_thread
):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.synchronize()
    default_category.save()

    response = user_client.get(reverse("misago:categories"))
    assert_contains(response, default_category.description)
    assert_contains(response, user_thread.title)


@override_dynamic_settings(index_view="threads")
def test_categories_view_displays_category_thread(
    default_category, user_client, thread
):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.synchronize()
    default_category.save()

    response = user_client.get(reverse("misago:categories"))
    assert_contains(response, default_category.description)
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="threads")
def test_categories_view_displays_unread_category(
    default_category, user_client, user, user_thread
):
    user.joined_on -= timedelta(days=2)
    user.save()

    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.synchronize()
    default_category.save()

    response = user_client.get(reverse("misago:categories"))
    assert_contains(response, default_category.description)
    assert_contains(response, user_thread.title)
    assert_contains(response, "Category has unread posts")


@override_dynamic_settings(index_view="threads")
def test_categories_view_displays_category_thread_if_category_allows_list_access(
    default_category, user, user_client, thread
):
    default_category.delay_browse_check = True
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.synchronize()
    default_category.save()

    remove_category_group_permissions(default_category, user.group)

    grant_category_group_permissions(
        default_category,
        user.group,
        CategoryPermission.SEE,
    )

    response = user_client.get(reverse("misago:categories"))
    assert_contains(response, default_category.description)
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="threads")
def test_categories_view_excludes_category_thread_if_user_has_no_browse_permission(
    default_category, user, user_client, thread
):
    default_category.description = "FIRST-CATEGORY-DESCRIPTION"
    default_category.synchronize()
    default_category.save()

    remove_category_group_permissions(default_category, user.group)

    grant_category_group_permissions(
        default_category,
        user.group,
        CategoryPermission.SEE,
    )

    response = user_client.get(reverse("misago:categories"))
    assert_contains(response, default_category.description)
    assert_not_contains(response, thread.title)


@override_dynamic_settings(index_view="threads")
def test_categories_view_displays_empty_list_for_guest(
    default_category, guests_group, client
):
    remove_category_group_permissions(default_category, guests_group)
    default_category.delete()

    response = client.get(reverse("misago:categories"))
    assert_contains(response, "No categories exist")


@override_dynamic_settings(index_view="threads")
def test_categories_view_displays_empty_list_for_user(
    default_category, user, user_client
):
    remove_category_group_permissions(default_category, user.group)
    default_category.delete()

    response = user_client.get(reverse("misago:categories"))
    assert_contains(response, "No categories exist")
