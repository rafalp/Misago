import pytest
from django.core.exceptions import PermissionDenied
from django.http import Http404

from ..attachments import (
    can_upload_private_threads_attachments,
    can_upload_threads_attachments,
    check_delete_attachment_permission,
    check_download_attachment_permission,
)
from ..enums import CanUploadAttachments, CategoryPermission
from ..models import CategoryGroupPermission, Moderator
from ..proxy import UserPermissionsProxy


def test_can_upload_threads_attachments_returns_true_if_user_has_permission(
    user, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)
    assert can_upload_threads_attachments(permissions, default_category)


def test_can_upload_threads_attachments_returns_true_if_user_has_permission_to_upload_in_threads(
    user, members_group, cache_versions, default_category
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    assert can_upload_threads_attachments(permissions, default_category)


def test_can_upload_threads_attachments_returns_false_if_user_cant_upload_attachments(
    user, members_group, cache_versions, default_category
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    assert not can_upload_threads_attachments(permissions, default_category)


def test_can_upload_threads_attachments_returns_false_if_user_is_missing_category_attachments_permission(
    user, members_group, cache_versions, default_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category,
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)
    assert not can_upload_threads_attachments(permissions, default_category)


def test_can_upload_private_threads_attachments_returns_true_if_user_has_permission(
    user, cache_versions
):
    permissions = UserPermissionsProxy(user, cache_versions)
    assert can_upload_private_threads_attachments(permissions)


def test_can_upload_private_threads_attachments_returns_false_if_user_has_permission_in_threads_only(
    user, members_group, cache_versions
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    assert not can_upload_private_threads_attachments(permissions)


def test_can_upload_private_threads_attachments_returns_false_if_user_cant_upload_attachments(
    user, members_group, cache_versions
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    assert not can_upload_private_threads_attachments(permissions)


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


def test_check_delete_attachment_permission_passes_misago_admin_for_unused_attachment(
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


def test_check_delete_attachment_permission_passes_global_moderator_for_unused_attachment(
    moderator, attachment, cache_versions
):
    permissions = UserPermissionsProxy(moderator, cache_versions)

    check_delete_attachment_permission(
        permissions,
        attachment.category,
        attachment.thread,
        attachment.post,
        attachment,
    )


def test_check_delete_attachment_permission_fails_category_moderator_for_unused_attachment(
    user, attachment, cache_versions
):
    Moderator.objects.create(
        user=user,
        is_global=False,
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_delete_attachment_permission(
            permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )


def test_check_delete_attachment_permission_passes_uploader_for_unused_attachment(
    user, attachment, cache_versions
):
    attachment.uploader = user
    attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    check_delete_attachment_permission(
        permissions,
        attachment.category,
        attachment.thread,
        attachment.post,
        attachment,
    )


def test_check_delete_attachment_permission_passes_misago_admin_for_thread_attachment(
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


def test_check_delete_attachment_permission_passes_global_moderator_for_thread_attachment(
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


def test_check_delete_attachment_permission_passes_category_moderator_for_thread_attachment(
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


def test_check_delete_attachment_permission_passes_uploader_for_thread_attachment(
    user, attachment, cache_versions, post
):
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.uploader = user
    attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    check_delete_attachment_permission(
        permissions,
        attachment.category,
        attachment.thread,
        attachment.post,
        attachment,
    )


def test_check_delete_attachment_permission_fails_uploader_without_permission_for_thread_attachment(
    user, members_group, attachment, cache_versions, post
):
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.uploader = user
    attachment.save()

    members_group.can_always_delete_own_attachments = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_delete_attachment_permission(
            permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )


def test_check_delete_attachment_permission_fails_user_for_other_users_thread_attachment(
    user, other_user, attachment, cache_versions, post
):
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.uploader = other_user
    attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_delete_attachment_permission(
            permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )


def test_check_delete_attachment_permission_passes_misago_admin_for_private_thread_attachment(
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


def test_check_delete_attachment_permission_passes_global_moderator_for_private_thread_attachment(
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


def test_check_delete_attachment_permission_passes_private_threads_moderator_for_private_thread_attachment(
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


def test_check_delete_attachment_permission_passes_uploader_for_private_thread_attachment(
    user, attachment, cache_versions, private_threads_category, private_thread
):
    attachment.category = private_threads_category
    attachment.thread = private_thread
    attachment.post = private_thread.first_post
    attachment.uploader = user
    attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    check_delete_attachment_permission(
        permissions,
        attachment.category,
        attachment.thread,
        attachment.post,
        attachment,
    )


def test_check_delete_attachment_permission_fails_uploader_without_permission_for_private_thread_attachment(
    user,
    members_group,
    attachment,
    cache_versions,
    private_threads_category,
    private_thread,
):
    attachment.category = private_threads_category
    attachment.thread = private_thread
    attachment.post = private_thread.first_post
    attachment.uploader = user
    attachment.save()

    members_group.can_always_delete_own_attachments = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_delete_attachment_permission(
            permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )


def test_check_delete_attachment_permission_fails_user_for_other_users_private_thread_attachment(
    user,
    other_user,
    attachment,
    cache_versions,
    private_threads_category,
    private_thread,
):
    attachment.category = private_threads_category
    attachment.thread = private_thread
    attachment.post = private_thread.first_post
    attachment.uploader = other_user
    attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_delete_attachment_permission(
            permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )


def test_check_delete_attachment_permission_fails_anonymous_user(
    anonymous_user, attachment, cache_versions, post
):
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_delete_attachment_permission(
            permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )
