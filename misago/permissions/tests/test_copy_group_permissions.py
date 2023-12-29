import pytest

from ..copy import copy_group_permissions
from ..models import CategoryGroupPermission


def test_copy_group_permissions_copies_category_permission(
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


def test_copy_group_permissions_deletes_previous_category_permission(
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
