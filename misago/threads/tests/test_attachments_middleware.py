from unittest.mock import Mock

import pytest
from rest_framework import serializers

from .. import test
from ...conf.test import override_dynamic_settings
from ..api.postingendpoint import PostingEndpoint
from ..api.postingendpoint.attachments import (
    AttachmentsMiddleware,
    validate_attachments_count,
)
from ..models import Attachment, AttachmentType


@pytest.fixture
def context(default_category, dynamic_settings, user, user_acl):
    thread = test.post_thread(category=default_category)
    post = thread.first_post
    post.update_fields = []

    return {
        "category": default_category,
        "thread": thread,
        "post": post,
        "settings": dynamic_settings,
        "user": user,
        "user_acl": user_acl,
    }


def create_attachment(*, post=None, user=None):
    return Attachment.objects.create(
        secret=Attachment.generate_new_secret(),
        filetype=AttachmentType.objects.order_by("id").last(),
        post=post,
        size=1000,
        uploader=user if user else None,
        uploader_name=user.username if user else "testuser",
        uploader_slug=user.slug if user else "testuser",
        filename="testfile_%s.zip" % (Attachment.objects.count() + 1),
    )


def test_middleware_is_used_if_user_has_permission_to_upload_attachments(context):
    context["user_acl"]["max_attachment_size"] = 1024
    middleware = AttachmentsMiddleware(**context)
    assert middleware.use_this_middleware()


def test_middleware_is_not_used_if_user_has_no_permission_to_upload_attachments(
    context
):
    context["user_acl"]["max_attachment_size"] = 0
    middleware = AttachmentsMiddleware(**context)
    assert not middleware.use_this_middleware()


def test_middleware_handles_no_data(context):
    middleware = AttachmentsMiddleware(
        request=Mock(data={}), mode=PostingEndpoint.START, **context
    )

    serializer = middleware.get_serializer()
    assert serializer.is_valid()


def test_middleware_handles_empty_data(context):
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": []}), mode=PostingEndpoint.START, **context
    )

    serializer = middleware.get_serializer()
    assert serializer.is_valid()


def test_data_validation_fails_if_attachments_data_is_not_iterable(context):
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": "none"}),
        mode=PostingEndpoint.START,
        **context
    )

    serializer = middleware.get_serializer()
    assert not serializer.is_valid()


def test_data_validation_fails_if_attachments_data_has_non_int_values(context):
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": [1, "b"]}),
        mode=PostingEndpoint.START,
        **context
    )

    serializer = middleware.get_serializer()
    assert not serializer.is_valid()


@override_dynamic_settings(post_attachments_limit=2)
def test_data_validation_fails_if_attachments_data_is_longer_than_allowed(context):
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": range(5)}),
        mode=PostingEndpoint.START,
        **context
    )

    serializer = middleware.get_serializer()
    assert not serializer.is_valid()


def test_middleware_adds_attachment_to_new_post(context):
    new_attachment = create_attachment(user=context["user"])
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": [new_attachment.id]}),
        mode=PostingEndpoint.START,
        **context
    )
    serializer = middleware.get_serializer()
    serializer.is_valid()
    middleware.save(serializer)

    new_attachment.refresh_from_db()
    assert new_attachment.post == context["post"]


def test_middleware_adds_attachment_to_attachments_cache(context):
    new_attachment = create_attachment(user=context["user"])
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": [new_attachment.id]}),
        mode=PostingEndpoint.START,
        **context
    )
    serializer = middleware.get_serializer()
    serializer.is_valid()
    middleware.save(serializer)

    attachments_cache = context["post"].attachments_cache
    assert len(attachments_cache) == 1
    assert attachments_cache[0]["id"] == new_attachment.id


def test_middleware_adds_attachment_to_existing_post(context):
    new_attachment = create_attachment(user=context["user"])
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": [new_attachment.id]}),
        mode=PostingEndpoint.EDIT,
        **context
    )
    serializer = middleware.get_serializer()
    serializer.is_valid()
    middleware.save(serializer)

    new_attachment.refresh_from_db()
    assert new_attachment.post == context["post"]


def test_middleware_adds_attachment_to_post_with_existing_attachment(context):
    old_attachment = create_attachment(post=context["post"])
    new_attachment = create_attachment(user=context["user"])
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": [old_attachment.id, new_attachment.id]}),
        mode=PostingEndpoint.EDIT,
        **context
    )
    serializer = middleware.get_serializer()
    serializer.is_valid()
    middleware.save(serializer)

    new_attachment.refresh_from_db()
    assert new_attachment.post == context["post"]

    old_attachment.refresh_from_db()
    assert old_attachment.post == context["post"]


def test_middleware_adds_attachment_to_existing_attachments_cache(context):
    old_attachment = create_attachment(post=context["post"])
    new_attachment = create_attachment(user=context["user"])
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": [old_attachment.id, new_attachment.id]}),
        mode=PostingEndpoint.EDIT,
        **context
    )
    serializer = middleware.get_serializer()
    serializer.is_valid()
    middleware.save(serializer)

    attachments_cache = context["post"].attachments_cache
    assert len(attachments_cache) == 2
    assert attachments_cache[0]["id"] == new_attachment.id
    assert attachments_cache[1]["id"] == old_attachment.id


def test_other_user_attachment_cant_be_added_to_post(context):
    attachment = create_attachment()
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": [attachment.id]}),
        mode=PostingEndpoint.EDIT,
        **context
    )
    serializer = middleware.get_serializer()
    serializer.is_valid()
    middleware.save(serializer)

    attachment.refresh_from_db()
    assert not attachment.post


def test_other_post_attachment_cant_be_added_to_new_post(context, default_category):
    post = test.post_thread(category=default_category).first_post
    attachment = create_attachment(post=post, user=context["user"])
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": [attachment.id]}),
        mode=PostingEndpoint.EDIT,
        **context
    )
    serializer = middleware.get_serializer()
    serializer.is_valid()
    middleware.save(serializer)

    attachment.refresh_from_db()
    assert attachment.post == post


def test_middleware_removes_attachment_from_post(context):
    attachment = create_attachment(post=context["post"], user=context["user"])
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": []}), mode=PostingEndpoint.EDIT, **context
    )
    serializer = middleware.get_serializer()
    serializer.is_valid()
    middleware.save(serializer)

    context["post"].refresh_from_db()
    assert not context["post"].attachment_set.exists()


def test_middleware_removes_attachment_from_attachments_cache(context):
    attachment = create_attachment(post=context["post"], user=context["user"])
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": []}), mode=PostingEndpoint.EDIT, **context
    )
    serializer = middleware.get_serializer()
    serializer.is_valid()
    middleware.save(serializer)

    assert not context["post"].attachments_cache


def test_middleware_deletes_attachment_removed_from_post(context):
    attachment = create_attachment(post=context["post"], user=context["user"])
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": []}), mode=PostingEndpoint.EDIT, **context
    )
    serializer = middleware.get_serializer()
    serializer.is_valid()
    middleware.save(serializer)

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()


def test_middleware_blocks_user_from_removing_other_user_attachment_without_permission(
    context
):
    attachment = create_attachment(post=context["post"])
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": []}), mode=PostingEndpoint.EDIT, **context
    )
    serializer = middleware.get_serializer()
    assert not serializer.is_valid()
    middleware.save(serializer)

    attachment.refresh_from_db()
    assert attachment.post == context["post"]


def test_middleware_allows_user_with_permission_to_remove_other_user_attachment(
    context
):
    context["user_acl"]["can_delete_other_users_attachments"] = True
    attachment = create_attachment(post=context["post"])
    middleware = AttachmentsMiddleware(
        request=Mock(data={"attachments": []}), mode=PostingEndpoint.EDIT, **context
    )
    serializer = middleware.get_serializer()
    serializer.is_valid()
    middleware.save(serializer)

    context["post"].refresh_from_db()
    assert not context["post"].attachment_set.exists()


def test_attachments_count_validator_allows_attachments_within_limit():
    settings = Mock(post_attachments_limit=5)
    validate_attachments_count(range(5), settings)


def test_attachments_count_validator_raises_validation_error_on_too_many_attachmes():
    settings = Mock(post_attachments_limit=2)
    with pytest.raises(serializers.ValidationError):
        validate_attachments_count(range(5), settings)
