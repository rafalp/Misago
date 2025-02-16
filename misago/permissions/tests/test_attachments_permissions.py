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
    user, cache_versions, user_text_attachment
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_download_attachment_permission(
        permissions, None, None, None, user_text_attachment
    )


def test_check_download_attachment_permission_fails_for_other_user_not_posted_attachment(
    user, cache_versions, other_user_text_attachment
):
    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions, None, None, None, other_user_text_attachment
        )


def test_check_download_attachment_permission_fails_for_anonymous_user_not_posted_attachment(
    user, cache_versions, text_attachment
):
    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions, None, None, None, text_attachment
        )


def test_check_download_attachment_permission_passes_for_other_user_not_posted_attachment_if_user_is_misago_admin(
    admin, cache_versions, other_user_text_attachment
):
    permissions = UserPermissionsProxy(admin, cache_versions)
    check_download_attachment_permission(
        permissions, None, None, None, other_user_text_attachment
    )


def test_check_download_attachment_permission_passes_for_anonymous_user_not_posted_attachment_if_user_is_misago_admin(
    admin, cache_versions, text_attachment
):
    permissions = UserPermissionsProxy(admin, cache_versions)
    check_download_attachment_permission(permissions, None, None, None, text_attachment)


def test_check_download_attachment_permission_passes_user_with_permission(
    user, cache_versions, text_attachment, post
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_download_attachment_permission(
        permissions,
        text_attachment.category,
        text_attachment.thread,
        text_attachment.post,
        text_attachment,
    )


def test_check_download_attachment_permission_fails_user_without_category_permission(
    user, members_group, cache_versions, text_attachment, default_category, post
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    CategoryGroupPermission.objects.filter(
        category=default_category,
        group=members_group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions,
            text_attachment.category,
            text_attachment.thread,
            text_attachment.post,
            text_attachment,
        )


def test_check_download_attachment_permission_fails_user_without_thread_permission(
    user, cache_versions, text_attachment, thread, post
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions,
            text_attachment.category,
            text_attachment.thread,
            text_attachment.post,
            text_attachment,
        )


def test_check_download_attachment_permission_fails_user_without_post_permission(
    user, cache_versions, text_attachment, post
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions,
            text_attachment.category,
            text_attachment.thread,
            text_attachment.post,
            text_attachment,
        )


def test_check_download_attachment_permission_fails_user_without_attachments_category_permission(
    user, members_group, cache_versions, text_attachment, default_category, post
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    CategoryGroupPermission.objects.filter(
        category=default_category,
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_download_attachment_permission(
            permissions,
            text_attachment.category,
            text_attachment.thread,
            text_attachment.post,
            text_attachment,
        )


def test_check_download_attachment_permission_passes_user_with_private_threads_permission(
    user, cache_versions, text_attachment, user_private_thread
):
    text_attachment.associate_with_post(user_private_thread.first_post)
    text_attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_download_attachment_permission(
        permissions,
        text_attachment.category,
        text_attachment.thread,
        text_attachment.post,
        text_attachment,
    )


def test_check_download_attachment_permission_fails_user_without_private_threads_permission(
    user,
    members_group,
    cache_versions,
    text_attachment,
    user_private_thread,
):
    text_attachment.associate_with_post(user_private_thread.first_post)
    text_attachment.save()

    members_group.can_use_private_threads = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions,
            text_attachment.category,
            text_attachment.thread,
            text_attachment.post,
            text_attachment,
        )


def test_check_download_attachment_permission_fails_user_without_private_thread_permission(
    user, cache_versions, text_attachment, private_thread
):
    text_attachment.associate_with_post(private_thread.first_post)
    text_attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_download_attachment_permission(
            permissions,
            text_attachment.category,
            text_attachment.thread,
            text_attachment.post,
            text_attachment,
        )


def test_check_delete_attachment_permission_passes_misago_admin_for_unused_attachment(
    admin, text_attachment, cache_versions
):
    permissions = UserPermissionsProxy(admin, cache_versions)

    check_delete_attachment_permission(
        permissions,
        text_attachment.category,
        text_attachment.thread,
        text_attachment.post,
        text_attachment,
    )


def test_check_delete_attachment_permission_passes_global_moderator_for_unused_attachment(
    moderator, text_attachment, cache_versions
):
    permissions = UserPermissionsProxy(moderator, cache_versions)

    check_delete_attachment_permission(
        permissions,
        text_attachment.category,
        text_attachment.thread,
        text_attachment.post,
        text_attachment,
    )


def test_check_delete_attachment_permission_fails_category_moderator_for_unused_attachment(
    user, text_attachment, cache_versions
):
    Moderator.objects.create(
        user=user,
        is_global=False,
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_delete_attachment_permission(
            permissions,
            text_attachment.category,
            text_attachment.thread,
            text_attachment.post,
            text_attachment,
        )


def test_check_delete_attachment_permission_passes_uploader_for_unused_attachment(
    user, text_attachment, cache_versions
):
    text_attachment.uploader = user
    text_attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    check_delete_attachment_permission(
        permissions,
        text_attachment.category,
        text_attachment.thread,
        text_attachment.post,
        text_attachment,
    )


def test_check_delete_attachment_permission_passes_misago_admin_for_thread_attachment(
    admin, text_attachment, cache_versions, post
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    permissions = UserPermissionsProxy(admin, cache_versions)

    check_delete_attachment_permission(
        permissions,
        text_attachment.category,
        text_attachment.thread,
        text_attachment.post,
        text_attachment,
    )


def test_check_delete_attachment_permission_passes_global_moderator_for_thread_attachment(
    moderator, text_attachment, cache_versions, post
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)

    check_delete_attachment_permission(
        permissions,
        text_attachment.category,
        text_attachment.thread,
        text_attachment.post,
        text_attachment,
    )


def test_check_delete_attachment_permission_passes_category_moderator_for_thread_attachment(
    user, text_attachment, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    text_attachment.associate_with_post(post)
    text_attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    check_delete_attachment_permission(
        permissions,
        text_attachment.category,
        text_attachment.thread,
        text_attachment.post,
        text_attachment,
    )


def test_check_delete_attachment_permission_passes_uploader_for_thread_attachment(
    user, user_text_attachment, cache_versions, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    check_delete_attachment_permission(
        permissions,
        user_text_attachment.category,
        user_text_attachment.thread,
        user_text_attachment.post,
        user_text_attachment,
    )


def test_check_delete_attachment_permission_fails_uploader_without_permission_for_thread_attachment(
    user, members_group, user_text_attachment, cache_versions, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    members_group.can_always_delete_own_attachments = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_delete_attachment_permission(
            permissions,
            user_text_attachment.category,
            user_text_attachment.thread,
            user_text_attachment.post,
            user_text_attachment,
        )


def test_check_delete_attachment_permission_fails_user_for_other_users_thread_attachment(
    user, other_user, other_user_text_attachment, cache_versions, post
):
    other_user_text_attachment.associate_with_post(post)
    other_user_text_attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_delete_attachment_permission(
            permissions,
            other_user_text_attachment.category,
            other_user_text_attachment.thread,
            other_user_text_attachment.post,
            other_user_text_attachment,
        )


def test_check_delete_attachment_permission_passes_misago_admin_for_private_thread_attachment(
    admin, text_attachment, cache_versions, private_thread
):
    text_attachment.associate_with_post(private_thread.first_post)
    text_attachment.save()

    permissions = UserPermissionsProxy(admin, cache_versions)

    check_delete_attachment_permission(
        permissions,
        text_attachment.category,
        text_attachment.thread,
        text_attachment.post,
        text_attachment,
    )


def test_check_delete_attachment_permission_passes_global_moderator_for_private_thread_attachment(
    moderator, text_attachment, cache_versions, private_thread
):
    text_attachment.associate_with_post(private_thread.first_post)
    text_attachment.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)

    check_delete_attachment_permission(
        permissions,
        text_attachment.category,
        text_attachment.thread,
        text_attachment.post,
        text_attachment,
    )


def test_check_delete_attachment_permission_passes_private_threads_moderator_for_private_thread_attachment(
    user, text_attachment, cache_versions, private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    text_attachment.associate_with_post(private_thread.first_post)
    text_attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    check_delete_attachment_permission(
        permissions,
        text_attachment.category,
        text_attachment.thread,
        text_attachment.post,
        text_attachment,
    )


def test_check_delete_attachment_permission_passes_uploader_for_private_thread_attachment(
    user, user_text_attachment, cache_versions, private_thread
):
    user_text_attachment.associate_with_post(private_thread.first_post)
    user_text_attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    check_delete_attachment_permission(
        permissions,
        user_text_attachment.category,
        user_text_attachment.thread,
        user_text_attachment.post,
        user_text_attachment,
    )


def test_check_delete_attachment_permission_fails_uploader_without_permission_for_private_thread_attachment(
    user,
    members_group,
    user_text_attachment,
    cache_versions,
    private_thread,
):
    user_text_attachment.associate_with_post(private_thread.first_post)
    user_text_attachment.save()

    members_group.can_always_delete_own_attachments = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_delete_attachment_permission(
            permissions,
            user_text_attachment.category,
            user_text_attachment.thread,
            user_text_attachment.post,
            user_text_attachment,
        )


def test_check_delete_attachment_permission_fails_user_for_other_users_private_thread_attachment(
    user,
    other_user_text_attachment,
    cache_versions,
    private_thread,
):
    other_user_text_attachment.associate_with_post(private_thread.first_post)
    other_user_text_attachment.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_delete_attachment_permission(
            permissions,
            other_user_text_attachment.category,
            other_user_text_attachment.thread,
            other_user_text_attachment.post,
            other_user_text_attachment,
        )


def test_check_delete_attachment_permission_fails_anonymous_user(
    anonymous_user, text_attachment, cache_versions, post
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_delete_attachment_permission(
            permissions,
            text_attachment.category,
            text_attachment.thread,
            text_attachment.post,
            text_attachment,
        )
