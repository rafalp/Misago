import pytest

from ...users.models import Group
from ..copy import COPY_GROUP_PERMISSIONS, copy_group_permissions
from ..enums import PermissionValue
from ..models import CategoryGroupPermission

GROUP_MODEL_NON_PERMISSION_FIELDS = (
    "id",
    "name",
    "slug",
    "description",
    "description_parsed",
    "meta_description",
    "user_title",
    "color",
    "icon",
    "css_suffix",
    "is_page",
    "is_hidden",
    "is_default",
    "ordering",
    "plugin_data",
    "categorygrouppermission",
    "moderator",
    "plugin_data",
    "user",
)


def test_copy_group_permissions_tuple_has_all_group_permission_fields():
    copied_permissions = set(COPY_GROUP_PERMISSIONS)
    group_permissions = set()

    for field in Group._meta.get_fields():
        if field.name not in GROUP_MODEL_NON_PERMISSION_FIELDS:
            group_permissions.add(field.name)

    assert not group_permissions.difference(copied_permissions)


def test_copy_group_permissions_copies_group_permissions(members_group, custom_group):
    assert custom_group.can_see_user_profiles == PermissionValue.NO

    copy_group_permissions(members_group, custom_group)

    assert custom_group.can_see_user_profiles == PermissionValue.YES

    custom_group.refresh_from_db()
    assert custom_group.can_see_user_profiles == PermissionValue.YES


def test_copy_group_permissions_copies_category_permissions(
    members_group, custom_group, other_category
):
    CategoryGroupPermission.objects.create(
        group=members_group,
        category=other_category,
        permission="test",
    )

    copy_group_permissions(members_group, custom_group)

    CategoryGroupPermission.objects.get(
        group=custom_group,
        category=other_category,
        permission="test",
    )


def test_copy_group_permissions_deletes_previous_category_permissions(
    members_group, custom_group, other_category
):
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=other_category,
        permission="deleted",
    )

    copy_group_permissions(members_group, custom_group)

    with pytest.raises(CategoryGroupPermission.DoesNotExist):
        CategoryGroupPermission.objects.get(
            group=custom_group,
            category=other_category,
            permission="deleted",
        )
