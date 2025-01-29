from ..models import Attachment
from ..storage import (
    get_total_attachment_storage_usage,
    get_total_unused_attachments_size,
    get_user_attachment_storage_usage,
    get_user_unused_attachments_size,
)


def test_get_total_attachment_storage_usage_returns_zero_if_no_attachments_exist(db):
    assert get_total_attachment_storage_usage() == 0


def test_get_total_attachment_storage_usage_returns_sum_of_all_attachments_sizes(post):
    Attachment.objects.create(
        category=post.category,
        thread=post.thread,
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=50,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=20,
        filetype_id="png",
        thumbnail_size=10,
    )

    assert get_total_attachment_storage_usage() == 80


def test_get_total_unused_attachments_size_returns_zero_if_no_attachments_exist(db):
    assert get_total_unused_attachments_size() == 0


def test_get_total_unused_attachments_size_returns_zero_if_no_unused_attachments_exist(
    post,
):
    Attachment.objects.create(
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=50,
        filetype_id="png",
    )

    assert get_total_unused_attachments_size() == 0


def test_get_total_unused_attachments_size_returns_sum_of_unused_attachments_sizes(db):
    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=50,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=20,
        filetype_id="png",
        thumbnail_size=10,
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=3,
        filetype_id="png",
        thumbnail_size=2,
    )

    assert get_total_unused_attachments_size() == 85


def test_get_total_unused_attachments_size_excludes_posted_attachments_sizes(post):
    Attachment.objects.create(
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=50,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=20,
        filetype_id="png",
        thumbnail_size=10,
    )

    assert get_total_unused_attachments_size() == 30


def test_get_user_attachment_storage_usage_returns_zero_if_no_attachments_exist(user):
    assert get_user_attachment_storage_usage(user) == 0


def test_get_user_attachment_storage_usage_excludes_anonymous_users_attachments(user):
    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=50,
        filetype_id="png",
    )

    assert get_user_attachment_storage_usage(user) == 0


def test_get_user_attachment_storage_usage_excludes_other_users_attachments(
    user, other_user
):
    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=other_user,
        name="image.png",
        slug="image-png",
        size=20,
        filetype_id="png",
        thumbnail_size=10,
    )

    assert get_user_attachment_storage_usage(user) == 0


def test_get_total_attachment_storage_usage_returns_sum_of_user_attachments_sizes(
    user, post
):
    Attachment.objects.create(
        category=post.category,
        thread=post.thread,
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=50,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=20,
        filetype_id="png",
        thumbnail_size=10,
    )

    assert get_user_attachment_storage_usage(user) == 80


def test_get_user_unused_attachments_size_returns_zero_if_no_attachments_exist(user):
    assert get_user_unused_attachments_size(user) == 0


def test_get_user_unused_attachments_size_excludes_anonymous_users_attachments(user):
    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=50,
        filetype_id="png",
    )

    assert get_user_unused_attachments_size(user) == 0


def test_get_user_unused_attachments_size_excludes_other_users_attachments(
    user, other_user
):
    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=other_user,
        name="image.png",
        slug="image-png",
        size=20,
        filetype_id="png",
        thumbnail_size=10,
    )

    assert get_user_unused_attachments_size(user) == 0


def test_get_user_unused_attachments_size_excludes_posted_attachments(user, post):
    Attachment.objects.create(
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        name="image.png",
        slug="image-png",
        size=20,
        filetype_id="png",
        thumbnail_size=10,
    )
    Attachment.objects.create(
        post=post,
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=20,
        filetype_id="png",
        thumbnail_size=10,
    )

    assert get_user_unused_attachments_size(user) == 0


def test_get_user_unused_attachments_size_returns_sum_of_user_attachments_sizes(
    user, post
):
    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=50,
        filetype_id="png",
    )

    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploader=user,
        name="image.png",
        slug="image-png",
        size=20,
        filetype_id="png",
        thumbnail_size=10,
    )

    assert get_user_attachment_storage_usage(user) == 80
