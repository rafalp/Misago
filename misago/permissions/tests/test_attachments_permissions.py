import pytest
from django.http import Http404

from ..attachments import (
    check_download_attachment_permission,
    get_private_threads_attachments_permissions,
    get_threads_attachments_permissions,
)
from ..enums import CanUploadAttachments, CategoryPermission
from ..models import CategoryGroupPermission, Moderator
from ..proxy import UserPermissionsProxy


def test_check_download_attachment_permission_passes_for_uploader_not_posted_attachment(
    user, cache_versions, user_attachment
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_download_attachment_permission(permissions, None, None, None, user_attachment)


def test_check_download_attachment_permission_fails_for_other_user_not_posted_attachment(
    user, cache_versions, other_user_attachment
):
    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions, None, None, None, other_user_attachment
        )


def test_check_download_attachment_permission_fails_for_anonymous_user_not_posted_attachment(
    user, cache_versions, attachment
):
    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(permissions, None, None, None, attachment)


def test_check_download_attachment_permission_passes_for_other_user_not_posted_attachment_if_user_is_misago_admin(
    admin, cache_versions, other_user_attachment
):
    permissions = UserPermissionsProxy(admin, cache_versions)
    check_download_attachment_permission(
        permissions, None, None, None, other_user_attachment
    )


def test_check_download_attachment_permission_passes_for_anonymous_user_not_posted_attachment_if_user_is_misago_admin(
    admin, cache_versions, attachment
):
    permissions = UserPermissionsProxy(admin, cache_versions)
    check_download_attachment_permission(permissions, None, None, None, attachment)


def test_get_threads_attachments_permissions_returns_permissions_object_for_user(
    user, cache_versions, default_category
):
    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert not permissions.is_moderator
    assert permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_user_without_upload_permission(
    user, members_group, cache_versions, default_category
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert not permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_user_without_upload_in_private_threads_permission(
    user, members_group, cache_versions, default_category
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert not permissions.is_moderator
    assert permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_user_without_delete_permission(
    user, members_group, cache_versions, default_category
):
    members_group.can_delete_own_attachments = False
    members_group.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert not permissions.is_moderator
    assert permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert not permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_user_without_category_attachments_permission(
    user, cache_versions, members_group, default_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category,
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert not permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert not permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_category_moderator(
    user, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert permissions.is_moderator
    assert permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_category_moderator_without_upload_permission(
    user, members_group, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_category_moderator_without_upload_in_private_threads_permission(
    user, members_group, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert permissions.is_moderator
    assert permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_category_moderator_without_delete_permission(
    user, members_group, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    members_group.can_delete_own_attachments = False
    members_group.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert permissions.is_moderator
    assert permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert not permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_category_moderator_without_category_attachments_permission(
    user, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    CategoryGroupPermission.objects.filter(
        permission=CategoryPermission.ATTACHMENTS
    ).delete()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert not permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert not permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_global_moderator(
    moderator, cache_versions, default_category
):
    proxy = UserPermissionsProxy(moderator, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert permissions.is_moderator
    assert permissions.can_upload_attachments
    assert not permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_global_moderator_without_upload_permission(
    moderator, moderators_group, cache_versions, default_category
):
    moderators_group.can_upload_attachments = CanUploadAttachments.NEVER
    moderators_group.save()

    proxy = UserPermissionsProxy(moderator, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert not permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_global_moderator_without_upload_in_private_threads_permission(
    moderator, moderators_group, cache_versions, default_category
):
    moderators_group.can_upload_attachments = CanUploadAttachments.THREADS
    moderators_group.save()

    proxy = UserPermissionsProxy(moderator, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert permissions.is_moderator
    assert permissions.can_upload_attachments
    assert not permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_global_moderator_without_delete_permission(
    moderator, moderators_group, cache_versions, default_category
):
    moderators_group.can_delete_own_attachments = False
    moderators_group.save()

    proxy = UserPermissionsProxy(moderator, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert permissions.is_moderator
    assert permissions.can_upload_attachments
    assert not permissions.attachment_size_limit
    assert not permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_global_moderator_without_category_attachments_permission(
    moderator, cache_versions, default_category
):
    CategoryGroupPermission.objects.filter(
        permission=CategoryPermission.ATTACHMENTS
    ).delete()

    proxy = UserPermissionsProxy(moderator, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert not permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert not permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_private_threads_moderator(
    user, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert not permissions.is_moderator
    assert permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_threads_attachments_permissions_returns_permissions_object_for_anonymous_user(
    anonymous_user, cache_versions, default_category
):
    proxy = UserPermissionsProxy(anonymous_user, cache_versions)
    proxy.permissions

    permissions = get_threads_attachments_permissions(proxy, default_category.id)
    assert not permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert not permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_user(
    user, cache_versions
):
    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert not permissions.is_moderator
    assert permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_user_without_upload_permission(
    user, members_group, cache_versions
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert not permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_user_without_upload_in_private_threads_permission(
    user, members_group, cache_versions
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert not permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_user_without_delete_permission(
    user, members_group, cache_versions
):
    members_group.can_delete_own_attachments = False
    members_group.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert not permissions.is_moderator
    assert permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert not permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_moderator(
    user, cache_versions
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert permissions.is_moderator
    assert permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_moderator_without_upload_permission(
    user, members_group, cache_versions
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_moderator_without_upload_in_private_threads_permission(
    user, members_group, cache_versions
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_moderator_without_delete_permission(
    user, members_group, cache_versions
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    members_group.can_delete_own_attachments = False
    members_group.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert permissions.is_moderator
    assert permissions.can_upload_attachments
    assert permissions.attachment_size_limit
    assert not permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_global_moderator(
    moderator, cache_versions
):
    proxy = UserPermissionsProxy(moderator, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert permissions.is_moderator
    assert permissions.can_upload_attachments
    assert not permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_global_moderator_without_upload_permission(
    moderator, moderators_group, cache_versions
):
    moderators_group.can_upload_attachments = CanUploadAttachments.NEVER
    moderators_group.save()

    proxy = UserPermissionsProxy(moderator, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert not permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_global_moderator_without_upload_in_private_threads_permission(
    moderator, moderators_group, cache_versions
):
    moderators_group.can_upload_attachments = CanUploadAttachments.THREADS
    moderators_group.save()

    proxy = UserPermissionsProxy(moderator, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert not permissions.attachment_size_limit
    assert permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_global_moderator_without_delete_permission(
    moderator, moderators_group, cache_versions
):
    moderators_group.can_delete_own_attachments = False
    moderators_group.save()

    proxy = UserPermissionsProxy(moderator, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert permissions.is_moderator
    assert permissions.can_upload_attachments
    assert not permissions.attachment_size_limit
    assert not permissions.can_delete_own_attachments


def test_get_private_threads_attachments_permissions_returns_permissions_object_for_anonymous_user(
    db, anonymous_user, cache_versions
):
    proxy = UserPermissionsProxy(anonymous_user, cache_versions)
    proxy.permissions

    permissions = get_private_threads_attachments_permissions(proxy)
    assert not permissions.is_moderator
    assert not permissions.can_upload_attachments
    assert not permissions.can_delete_own_attachments
