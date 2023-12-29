import pytest

from ..copy import copy_category_permissions
from ..models import CategoryGroupPermission


def test_copy_category_permissions_copies_category_permission(
    members_group, sibling_category, other_category
):
    CategoryGroupPermission.objects.create(
        group=members_group,
        category=sibling_category,
        permission="test",
    )

    copy_category_permissions(sibling_category, other_category)

    CategoryGroupPermission.objects.get(
        group=members_group,
        category=other_category,
        permission="test",
    )


def test_copy_category_permissions_deletes_previous_category_permission(
    members_group, sibling_category, other_category
):
    CategoryGroupPermission.objects.create(
        group=members_group,
        category=other_category,
        permission="deleted",
    )

    copy_category_permissions(sibling_category, other_category)

    with pytest.raises(CategoryGroupPermission.DoesNotExist):
        CategoryGroupPermission.objects.get(
            group=members_group,
            category=other_category,
            permission="deleted",
        )
