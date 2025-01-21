import pytest
from django.core.exceptions import PermissionDenied
from django.http import Http404

from ..attachments import (
    check_delete_attachment_permission,
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


def test_check_download_attachment_permission_passes_user_with_permission(
    user, cache_versions, attachment, default_category, thread, post
):
    attachment.category = default_category
    attachment.thread = thread
    attachment.post = post
    attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_download_attachment_permission(
        permissions, attachment.category, attachment.thread, attachment.post, attachment
    )


def test_check_download_attachment_permission_fails_user_without_category_permission(
    user, members_group, cache_versions, attachment, default_category, thread, post
):
    attachment.category = default_category
    attachment.thread = thread
    attachment.post = post
    attachment.save()

    CategoryGroupPermission.objects.filter(
        category=default_category,
        group=members_group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )


def test_check_download_attachment_permission_fails_user_without_thread_permission(
    user, cache_versions, attachment, default_category, thread, post
):
    attachment.category = default_category
    attachment.thread = thread
    attachment.post = post
    attachment.save()

    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )


def test_check_download_attachment_permission_fails_user_without_post_permission(
    user, cache_versions, attachment, default_category, thread, post
):
    attachment.category = default_category
    attachment.thread = thread
    attachment.post = post
    attachment.save()

    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )


def test_check_download_attachment_permission_fails_user_without_attachments_category_permission(
    user, members_group, cache_versions, attachment, default_category, thread, post
):
    attachment.category = default_category
    attachment.thread = thread
    attachment.post = post
    attachment.save()

    CategoryGroupPermission.objects.filter(
        category=default_category,
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_download_attachment_permission(
            permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )


def test_check_download_attachment_permission_passes_user_with_private_threads_permission(
    user, cache_versions, attachment, private_threads_category, user_private_thread
):
    attachment.category = private_threads_category
    attachment.thread = user_private_thread
    attachment.post = user_private_thread.first_post
    attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_download_attachment_permission(
        permissions, attachment.category, attachment.thread, attachment.post, attachment
    )


def test_check_download_attachment_permission_fails_user_without_private_threads_permission(
    user,
    members_group,
    cache_versions,
    attachment,
    private_threads_category,
    user_private_thread,
):
    attachment.category = private_threads_category
    attachment.thread = user_private_thread
    attachment.post = user_private_thread.first_post
    attachment.save()

    members_group.can_use_private_threads = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )


def test_check_download_attachment_permission_fails_user_without_private_thread_permission(
    user, cache_versions, attachment, private_threads_category, private_thread
):
    attachment.category = private_threads_category
    attachment.thread = private_thread
    attachment.post = private_thread.first_post
    attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )


def check_delete_attachment_permission_passes_misago_admin_form_unused_attachment(
    admin, attachment, cache_versions
):
    permissions = UserPermissionsProxy(admin, cache_versions)

    check_delete_attachment_permission(
        permissions,
        attachment.category,
        attachment.thread,
        attachment.post,
        attachment,
    )


def check_delete_attachment_permission_passes_misago_admin_for_thread_attachment(
    admin, attachment, cache_versions, post
):
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    permissions = UserPermissionsProxy(admin, cache_versions)

    check_delete_attachment_permission(
        permissions,
        attachment.category,
        attachment.thread,
        attachment.post,
        attachment,
    )


def check_delete_attachment_permission_passes_global_moderator_for_thread_attachment(
    moderator, attachment, cache_versions, post
):
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)

    check_delete_attachment_permission(
        permissions,
        attachment.category,
        attachment.thread,
        attachment.post,
        attachment,
    )


def check_delete_attachment_permission_passes_category_moderator_for_thread_attachment(
    user, attachment, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    check_delete_attachment_permission(
        permissions,
        attachment.category,
        attachment.thread,
        attachment.post,
        attachment,
    )


def check_delete_attachment_permission_passes_misago_admin_for_private_thread_attachment(
    admin, attachment, cache_versions, private_threads_category, private_thread
):
    attachment.category = private_threads_category
    attachment.thread = private_thread
    attachment.post = private_thread.first_post
    attachment.save()

    permissions = UserPermissionsProxy(admin, cache_versions)

    check_delete_attachment_permission(
        permissions,
        attachment.category,
        attachment.thread,
        attachment.post,
        attachment,
    )


def check_delete_attachment_permission_passes_global_moderator_for_private_thread_attachment(
    moderator, attachment, cache_versions, private_threads_category, private_thread
):
    attachment.category = private_threads_category
    attachment.thread = private_thread
    attachment.post = private_thread.first_post
    attachment.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)

    check_delete_attachment_permission(
        permissions,
        attachment.category,
        attachment.thread,
        attachment.post,
        attachment,
    )


def check_delete_attachment_permission_passes_private_threads_moderator_for_private_thread_attachment(
    user, attachment, cache_versions, private_threads_category, private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    attachment.category = private_threads_category
    attachment.thread = private_thread
    attachment.post = private_thread.first_post
    attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    check_delete_attachment_permission(
        permissions,
        attachment.category,
        attachment.thread,
        attachment.post,
        attachment,
    )


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
