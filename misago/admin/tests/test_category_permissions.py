import pytest
from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_has_error_message


def test_category_permissions_form_is_rendered(
    admin_client, custom_group, sibling_category
):
    response = admin_client.get(
        reverse(
            "misago:admin:categories:permissions", kwargs={"pk": sibling_category.id}
        )
    )
    assert_contains(response, sibling_category.name)
    assert_contains(response, custom_group.name)


def test_category_permissions_form_replaces_old_category_permissions_with_new(
    admin_client, custom_group, sibling_category
):
    see_permission = CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.SEE,
    )

    response = admin_client.post(
        reverse(
            "misago:admin:categories:permissions", kwargs={"pk": sibling_category.id}
        ),
        {f"permissions[{custom_group.id}]": [CategoryPermission.BROWSE]},
    )
    assert response.status_code == 302

    with pytest.raises(CategoryGroupPermission.DoesNotExist):
        see_permission.refresh_from_db()

    CategoryGroupPermission.objects.get(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.BROWSE,
    )


def test_category_permissions_form_invalidates_permissions_cache(
    admin_client, custom_group, sibling_category
):
    with assert_invalidates_cache(CacheName.PERMISSIONS):
        admin_client.post(
            reverse(
                "misago:admin:categories:permissions",
                kwargs={"pk": sibling_category.id},
            ),
            {f"permissions[{custom_group.id}]": [CategoryPermission.BROWSE]},
        )


def test_category_permissions_form_handles_not_existing_category_id(
    admin_client, sibling_category
):
    response = admin_client.get(
        reverse(
            "misago:admin:categories:permissions",
            kwargs={"pk": sibling_category.id + 1000},
        )
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested category does not exist.")
