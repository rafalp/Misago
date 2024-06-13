from ..enums import CategoryPermission
from ..models import CategoryGroupPermission
from ..user import build_user_category_permissions


def test_build_user_category_permissions_returns_no_permissions_for_user_without_perms(
    custom_group, default_category
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
    custom_group, default_category, sibling_category, child_category
):
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.SEE,
    )

    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [sibling_category.id],
        CategoryPermission.BROWSE: [],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_includes_group_see_and_browse_permissions(
    custom_group, default_category, sibling_category, child_category
):
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.BROWSE,
    )

    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [sibling_category.id],
        CategoryPermission.BROWSE: [sibling_category.id],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_requires_see_permission_for_browse_permissions(
    custom_group, sibling_category, child_category
):
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.BROWSE,
    )

    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [],
        CategoryPermission.BROWSE: [],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_checks_allow_list_access_if_browse_is_missing(
    custom_group, sibling_category, child_category
):
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=child_category,
        permission=CategoryPermission.SEE,
    )

    sibling_category.allow_list_access = True
    sibling_category.save()

    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [sibling_category.id, child_category.id],
        CategoryPermission.BROWSE: [],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_includes_all_permissions(
    custom_group, sibling_category, child_category
):
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.BROWSE,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.START,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.REPLY,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.ATTACHMENTS,
    )

    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [sibling_category.id],
        CategoryPermission.BROWSE: [sibling_category.id],
        CategoryPermission.START: [sibling_category.id],
        CategoryPermission.REPLY: [sibling_category.id],
        CategoryPermission.ATTACHMENTS: [sibling_category.id],
    }


def test_build_user_category_permissions_requires_browse_permissions_for_other_permissions(
    custom_group, sibling_category, child_category
):
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.START,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.REPLY,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
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
    custom_group, sibling_category, child_category
):
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=child_category,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=child_category,
        permission=CategoryPermission.BROWSE,
    )

    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [],
        CategoryPermission.BROWSE: [],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_child_category_is_visible_under_visible_parent(
    custom_group, sibling_category, child_category
):
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.BROWSE,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=child_category,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=child_category,
        permission=CategoryPermission.BROWSE,
    )

    permissions = build_user_category_permissions([custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [sibling_category.id, child_category.id],
        CategoryPermission.BROWSE: [sibling_category.id, child_category.id],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }


def test_build_user_category_permissions_combines_multiple_groups_permissions(
    members_group, custom_group, default_category, sibling_category, child_category
):
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=sibling_category,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        group=members_group,
        category=sibling_category,
        permission=CategoryPermission.BROWSE,
    )
    CategoryGroupPermission.objects.create(
        group=custom_group,
        category=child_category,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        group=members_group,
        category=child_category,
        permission=CategoryPermission.BROWSE,
    )

    permissions = build_user_category_permissions([members_group, custom_group], {})
    assert permissions == {
        CategoryPermission.SEE: [
            default_category.id,
            sibling_category.id,
            child_category.id,
        ],
        CategoryPermission.BROWSE: [
            default_category.id,
            sibling_category.id,
            child_category.id,
        ],
        CategoryPermission.START: [default_category.id],
        CategoryPermission.REPLY: [default_category.id],
        CategoryPermission.ATTACHMENTS: [default_category.id],
    }
