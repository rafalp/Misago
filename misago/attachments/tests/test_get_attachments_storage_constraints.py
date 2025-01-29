from ...permissions.proxy import UserPermissionsProxy
from ..enums import AttachmentStorage
from ..models import Attachment
from ..validators import get_attachments_storage_constraints


def test_get_attachments_storage_constraints_returns_no_constraint_if_all_limits_are_disabled(
    user, members_group, cache_versions
):
    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    storage_constraints = get_attachments_storage_constraints(0, permissions)
    assert storage_constraints == {
        "storage": None,
        "storage_limit": 0,
        "storage_left": 0,
    }


def test_get_attachments_storage_constraints_returns_global_constraint_if_user_limits_are_disabled(
    user, members_group, cache_versions
):
    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    storage_constraints = get_attachments_storage_constraints(1, permissions)
    assert storage_constraints == {
        "storage": AttachmentStorage.GLOBAL,
        "storage_limit": 1024 * 1024,
        "storage_left": 1024 * 1024,
    }


def test_get_attachments_storage_constraints_returns_user_unused_constraint_if_other_limits_are_disabled(
    user, members_group, cache_versions
):
    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 1
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    storage_constraints = get_attachments_storage_constraints(0, permissions)
    assert storage_constraints == {
        "storage": AttachmentStorage.USER_UNUSED,
        "storage_limit": 1024 * 1024,
        "storage_left": 1024 * 1024,
    }


def test_get_attachments_storage_constraints_counts_all_unused_attachments_to_global_limit(
    user, members_group, cache_versions, post
):
    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    Attachment.objects.create(
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=1024 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=512 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=128 * 1024,
        filetype_id="png",
        thumbnail_size=128 * 1024,
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    storage_constraints = get_attachments_storage_constraints(1, permissions)
    assert storage_constraints == {
        "storage": AttachmentStorage.GLOBAL,
        "storage_limit": 1024 * 1024,
        "storage_left": 256 * 1024,
    }


def test_get_attachments_storage_constraints_counts_all_user_attachments_to_user_total_limit(
    user, other_user, members_group, cache_versions, post
):
    members_group.attachment_storage_limit = 1
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    Attachment.objects.create(
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=other_user,
        name="image.png",
        slug="image-png",
        size=1024 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=1024 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=512 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=128 * 1024,
        filetype_id="png",
        thumbnail_size=128 * 1024,
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    storage_constraints = get_attachments_storage_constraints(0, permissions)
    assert storage_constraints == {
        "storage": AttachmentStorage.USER_TOTAL,
        "storage_limit": 1024 * 1024,
        "storage_left": 256 * 1024,
    }


def test_get_attachments_storage_constraints_counts_unused_user_attachments_to_user_unused_limit(
    user, other_user, members_group, cache_versions, post
):
    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 1
    members_group.save()

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=other_user,
        name="image.png",
        slug="image-png",
        size=1024 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=1024 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=512 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=128 * 1024,
        filetype_id="png",
        thumbnail_size=128 * 1024,
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    storage_constraints = get_attachments_storage_constraints(0, permissions)
    assert storage_constraints == {
        "storage": AttachmentStorage.USER_UNUSED,
        "storage_limit": 1024 * 1024,
        "storage_left": 768 * 1024,
    }


def test_get_attachments_storage_constraints_never_returns_negative_storage_left(
    user, members_group, cache_versions
):
    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=5 * 1024 * 1024,
        filetype_id="png",
        thumbnail_size=128 * 1024,
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    storage_constraints = get_attachments_storage_constraints(1, permissions)
    assert storage_constraints == {
        "storage": AttachmentStorage.GLOBAL,
        "storage_limit": 1024 * 1024,
        "storage_left": 0,
    }


def test_get_attachments_storage_constraints_returns_global_limit_because_its_smallest(
    user, other_user, members_group, cache_versions, post
):
    members_group.attachment_storage_limit = 1
    members_group.unused_attachments_storage_limit = 1
    members_group.save()

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=other_user,
        name="image.png",
        slug="image-png",
        size=700 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=512 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=100 * 1024,
        filetype_id="png",
        thumbnail_size=100 * 1024,
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    storage_constraints = get_attachments_storage_constraints(1, permissions)
    assert storage_constraints == {
        "storage": AttachmentStorage.GLOBAL,
        "storage_limit": 1024 * 1024,
        "storage_left": 124 * 1024,
    }


def test_get_attachments_storage_constraints_returns_user_total_limit_because_its_smallest(
    user, other_user, members_group, cache_versions, post
):
    members_group.attachment_storage_limit = 1
    members_group.unused_attachments_storage_limit = 1
    members_group.save()

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=other_user,
        name="image.png",
        slug="image-png",
        size=100 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=512 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=128 * 1024,
        filetype_id="png",
        thumbnail_size=128 * 1024,
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    storage_constraints = get_attachments_storage_constraints(1, permissions)
    assert storage_constraints == {
        "storage": AttachmentStorage.USER_TOTAL,
        "storage_limit": 1024 * 1024,
        "storage_left": 256 * 1024,
    }


def test_get_attachments_storage_constraints_returns_user_unused_limit_because_its_smallest(
    user, other_user, members_group, cache_versions, post
):
    members_group.attachment_storage_limit = 5
    members_group.unused_attachments_storage_limit = 1
    members_group.save()

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=other_user,
        name="image.png",
        slug="image-png",
        size=128 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=512 * 1024,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=256 * 1024,
        filetype_id="png",
        thumbnail_size=256 * 1024,
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    storage_constraints = get_attachments_storage_constraints(2, permissions)
    assert storage_constraints == {
        "storage": AttachmentStorage.USER_UNUSED,
        "storage_limit": 1024 * 1024,
        "storage_left": 512 * 1024,
    }
