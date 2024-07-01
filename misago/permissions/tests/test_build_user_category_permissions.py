from ..enums import CategoryPermission
from ..models import CategoryGroupPermission
from ..user import build_user_category_permissions


def test_build_user_category_permissions_returns_no_permissions_for_user_without_perms(
    custom_group, category
):
    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [],
        CategoryPermission.BROWSE: [],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_includes_group_see_permission(
    custom_group,
    category,
    category_custom_see_permission,
):
    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [category.id],
        CategoryPermission.BROWSE: [],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_includes_group_see_and_browse_permissions(
    custom_group,
    category,
    category_custom_see_permission,
    category_custom_browse_permission,
):
    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [category.id],
        CategoryPermission.BROWSE: [category.id],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_requires_see_permission_for_browse_permissions(
    custom_group,
    category,
    category_custom_browse_permission,
):
    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [],
        CategoryPermission.BROWSE: [],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_uses_delay_browse_check_if_browse_is_missing(
    custom_group,
    category,
    child_category,
    category_custom_see_permission,
    child_category_custom_see_permission,
):
    category.delay_browse_check = True
    category.save()

    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [category.id, child_category.id],
        CategoryPermission.BROWSE: [],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_includes_all_permissions(
    custom_group, category, child_category
):
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=category,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=category,
        permission=CategoryPermission.BROWSE,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=category,
        permission=CategoryPermission.START,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=category,
        permission=CategoryPermission.REPLY,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=category,
        permission=CategoryPermission.ATTACHMENTS,
    )

    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [category.id],
        CategoryPermission.BROWSE: [category.id],
        CategoryPermission.START: [category.id],
        CategoryPermission.REPLY: [category.id],
        CategoryPermission.ATTACHMENTS: [category.id],
    }


def test_build_user_category_permissions_requires_browse_permissions_for_other_permissions(
    custom_group, category, child_category
):
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=category,
        permission=CategoryPermission.START,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=category,
        permission=CategoryPermission.REPLY,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=category,
        permission=CategoryPermission.ATTACHMENTS,
    )

    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [],
        CategoryPermission.BROWSE: [],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_requires_parent_category_browse(
    custom_group,
    category,
    child_category,
    child_category_custom_see_permission,
    child_category_custom_browse_permission,
):
    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [],
        CategoryPermission.BROWSE: [],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_child_category_is_visible_under_visible_parent(
    custom_group,
    category,
    child_category,
    category_custom_see_permission,
    category_custom_browse_permission,
    child_category_custom_see_permission,
    child_category_custom_browse_permission,
):
    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [category.id, child_category.id],
        CategoryPermission.BROWSE: [category.id, child_category.id],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_combines_multiple_groups_permissions(
    members_group,
    custom_group,
    default_category,
    category,
    child_category,
    category_custom_see_permission,
    category_custom_browse_permission,
    child_category_custom_see_permission,
    child_category_custom_browse_permission,
):
    permissions = build_user_category_permissions([members_group, custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [
            default_category.id,
            category.id,
            child_category.id,
        ],
        CategoryPermission.BROWSE: [
            default_category.id,
            category.id,
            child_category.id,
        ],
        CategoryPermission.START: [default_category.id],
        CategoryPermission.REPLY: [default_category.id],
        CategoryPermission.ATTACHMENTS: [default_category.id],
    }
