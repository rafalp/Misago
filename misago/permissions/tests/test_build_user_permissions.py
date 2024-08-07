from ..enums import CategoryPermission
from ..user import build_user_permissions


def test_build_user_permissions_builds_user_permissions(user):
    permissions = build_user_permissions(user)
    assert permissions["can_see_user_profiles"]


def test_build_user_permissions_builds_user_permissions_from_multiple_groups(
    user, members_group, custom_group
):
    members_group.can_see_user_profiles = False
    members_group.save()

    custom_group.can_see_user_profiles = True
    custom_group.save()

    user.set_groups(members_group, [custom_group])
    user.save()

    permissions = build_user_permissions(user)
    assert permissions["can_see_user_profiles"]


def test_build_user_permissions_builds_anonymous_user_permissions(db, anonymous_user):
    permissions = build_user_permissions(anonymous_user)
    assert permissions["can_see_user_profiles"]


def test_build_user_permissions_builds_user_category_permissions(
    user, default_category
):
    permissions = build_user_permissions(user)
    assert permissions["categories"] == {
        CategoryPermission.SEE: [default_category.id],
        CategoryPermission.BROWSE: [default_category.id],
        CategoryPermission.START: [default_category.id],
        CategoryPermission.REPLY: [default_category.id],
        CategoryPermission.ATTACHMENTS: [default_category.id],
    }


def test_build_user_permissions_builds_anonymous_user_category_permissions(
    anonymous_user, default_category
):
    permissions = build_user_permissions(anonymous_user)
    assert permissions["categories"] == {
        CategoryPermission.SEE: [default_category.id],
        CategoryPermission.BROWSE: [default_category.id],
        CategoryPermission.START: [default_category.id],
        CategoryPermission.REPLY: [default_category.id],
        CategoryPermission.ATTACHMENTS: [default_category.id],
    }
