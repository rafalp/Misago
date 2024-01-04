import pytest
from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...categories.models import Category
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_has_error_message, assert_has_info_message


def test_group_category_permissions_form_is_rendered(
    admin_client, custom_group, sibling_category
):
    response = admin_client.get(
        reverse("misago:admin:groups:categories", kwargs={"pk": custom_group.id})
    )
    assert_contains(response, custom_group.name)
    assert_contains(response, sibling_category.name)


def test_group_category_permissions_form_replaces_old_category_permissions_with_new(
    admin_client, custom_group, sibling_category
):
    see_permission = CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.SEE,
    )

    response = admin_client.post(
        reverse("misago:admin:groups:categories", kwargs={"pk": custom_group.id}),
        {f"permissions[{sibling_category.id}]": [CategoryPermission.BROWSE]},
    )
    assert response.status_code == 302

    with pytest.raises(CategoryGroupPermission.DoesNotExist):
        see_permission.refresh_from_db()

    CategoryGroupPermission.objects.get(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.BROWSE,
    )


def test_group_category_permissions_form_invalidates_permissions_cache(
    admin_client, custom_group, sibling_category
):
    with assert_invalidates_cache(CacheName.PERMISSIONS):
        admin_client.post(
            reverse("misago:admin:groups:categories", kwargs={"pk": custom_group.id}),
            {f"permissions[{sibling_category.id}]": [CategoryPermission.BROWSE]},
        )


def test_group_category_permissions_form_redirects_to_groups_list_if_no_categories_exist(
    admin_client, custom_group
):
    Category.objects.filter(level__gt=0).delete()

    response = admin_client.get(
        reverse("misago:admin:groups:categories", kwargs={"pk": custom_group.id})
    )
    assert response.status_code == 302
    assert_has_info_message(
        response, "No categories exist to set group permissions for."
    )


def test_group_category_permissions_form_handles_not_existing_group_id(
    admin_client, custom_group
):
    response = admin_client.get(
        reverse(
            "misago:admin:groups:categories",
            kwargs={"pk": custom_group.id + 1000},
        )
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested group does not exist.")
