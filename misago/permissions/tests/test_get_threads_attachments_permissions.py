from ..enums import CategoryPermission
from ..models import CategoryGroupPermission
from ..proxy import UserPermissionsProxy


def test_get_attachments_permissions_returns_permissions_object_for_user(
    user, cache_versions, default_category
):
    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = proxy.get_attachments_permissions(default_category.id)
    assert not permissions.is_moderator
    assert permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_attachments_permissions_returns_permissions_object_for_user_without_category_attachments_permissison(
    user, cache_versions, members_group, default_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category,
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = proxy.get_attachments_permissions(default_category.id)
    assert not permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert not permissions.can_delete_own_attachments


def test_get_attachments_permissions_returns_permissions_object_for_moderator(
    moderator, cache_versions, default_category
):
    proxy = UserPermissionsProxy(moderator, cache_versions)
    proxy.permissions

    permissions = proxy.get_attachments_permissions(default_category.id)
    assert permissions.is_moderator
    assert permissions.can_upload_attachments
    assert not permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_attachments_permissions_returns_permissions_object_for_moderator_without_category_attachments_permissison(
    moderator, cache_versions, default_category
):
    CategoryGroupPermission.objects.filter(
        permission=CategoryPermission.ATTACHMENTS
    ).delete()

    proxy = UserPermissionsProxy(moderator, cache_versions)
    proxy.permissions

    permissions = proxy.get_attachments_permissions(default_category.id)
    assert not permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert not permissions.can_delete_own_attachments


def test_get_attachments_permissions_returns_permissions_object_for_anonymous_user(
    anonymous_user, cache_versions, default_category
):
    proxy = UserPermissionsProxy(anonymous_user, cache_versions)
    proxy.permissions

    permissions = proxy.get_attachments_permissions(default_category.id)
    assert not permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert not permissions.can_delete_own_attachments
