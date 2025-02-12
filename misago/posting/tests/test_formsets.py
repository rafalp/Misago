from unittest.mock import Mock

from django.http import HttpRequest

from ...attachments.enums import AllowedAttachments
from ...conf.test import override_dynamic_settings
from ...permissions.enums import CanUploadAttachments
from ...permissions.proxy import UserPermissionsProxy
from ..forms import PostForm, PostingForm
from ..formsets import (
    PostingFormset,
    get_edit_private_thread_formset,
    get_edit_private_thread_post_formset,
    get_edit_thread_formset,
    get_edit_thread_post_formset,
    get_reply_private_thread_formset,
    get_reply_thread_formset,
    get_start_private_thread_formset,
    get_start_thread_formset,
)


def test_posting_formset_is_request_preview_method_returns_false_for_not_post_request(
    rf,
):
    request = rf.get("/")
    formset = PostingFormset()
    assert not formset.is_request_preview(request)


def test_posting_formset_is_request_preview_method_returns_false_for_post_request_without_preview(
    rf,
):
    request = rf.post("/")
    formset = PostingFormset()
    assert not formset.is_request_preview(request)


def test_posting_formset_is_request_preview_method_returns_true_for_post_request(rf):
    request = rf.post("/", {PostingFormset.preview_action: "1"})
    formset = PostingFormset()
    assert formset.is_request_preview(request)


def test_posting_formset_is_request_upload_method_returns_false_for_not_post_request(
    rf,
):
    request = rf.get("/")
    formset = PostingFormset()
    assert not formset.is_request_upload(request)


class UploadForm(PostingForm):
    def is_request_upload(self, request: HttpRequest) -> bool:
        return PostForm.is_request_upload(request)


def test_posting_formset_is_request_upload_method_returns_false_for_post_request_without_upload(
    rf,
):
    request = rf.post("/")
    formset = PostingFormset()
    formset.add_form(UploadForm(prefix="test"))

    assert not formset.is_request_upload(request)


def test_posting_formset_is_request_upload_method_returns_true_for_post_request_with_upload(
    rf,
):
    request = rf.post("/", {PostForm.upload_action: "1"})
    formset = PostingFormset()
    formset.add_form(UploadForm(prefix="test"))

    assert formset.is_request_upload(request)


def test_get_start_thread_formset_initializes_valid_forms(
    user, cache_versions, dynamic_settings, default_category
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_start_thread_formset(request, default_category)
    assert formset.title
    assert formset.post
    assert not formset.invite_users


def test_get_start_thread_formset_setups_post_form_with_attachment_uploads(
    user, cache_versions, dynamic_settings, default_category
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_start_thread_formset(request, default_category)
    assert formset.post.show_attachments_upload


def test_get_start_thread_formset_setups_post_form_with_attachment_upload_if_uploads_are_limited_to_threads(
    user, members_group, cache_versions, dynamic_settings, default_category
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_start_thread_formset(request, default_category)
    assert formset.post.show_attachments_upload


def test_get_start_thread_formset_setups_post_form_without_attachment_upload_if_user_has_no_permission(
    user, members_group, cache_versions, dynamic_settings, default_category
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_start_thread_formset(request, default_category)
    assert not formset.post.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE)
def test_get_start_thread_formset_setups_post_form_without_attachment_upload_if_uploads_are_disabled(
    user, cache_versions, dynamic_settings, default_category
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_start_thread_formset(request, default_category)
    assert not formset.post.show_attachments_upload


def test_get_start_private_thread_formset_initializes_valid_forms(
    user, cache_versions, dynamic_settings, private_threads_category
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_start_private_thread_formset(request, private_threads_category)
    assert formset.title
    assert formset.post
    assert formset.invite_users


def test_get_start_private_thread_formset_setups_post_form_with_attachment_uploads(
    user, cache_versions, dynamic_settings, private_threads_category
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_start_private_thread_formset(request, private_threads_category)
    assert formset.post.show_attachments_upload


def test_get_start_private_thread_formset_setups_post_form_without_attachment_upload_if_uploads_are_limited_to_threads(
    user, members_group, cache_versions, dynamic_settings, private_threads_category
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_start_private_thread_formset(request, private_threads_category)
    assert not formset.post.show_attachments_upload


def test_get_start_private_thread_formset_setups_post_form_without_attachment_upload_if_user_no_permission(
    user, members_group, cache_versions, dynamic_settings, private_threads_category
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_start_private_thread_formset(request, private_threads_category)
    assert not formset.post.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE)
def test_get_start_private_thread_formset_setups_post_form_without_attachment_upload_if_uploads_are_disabled(
    user, cache_versions, dynamic_settings, private_threads_category
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_start_private_thread_formset(request, private_threads_category)
    assert not formset.post.show_attachments_upload


@override_dynamic_settings(allow_private_threads_attachments=False)
def test_get_start_private_thread_formset_setups_post_form_without_attachment_upload_if_private_threads_uploads_are_disabled(
    user, cache_versions, dynamic_settings, private_threads_category
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_start_private_thread_formset(request, private_threads_category)
    assert not formset.post.show_attachments_upload


def test_get_reply_thread_formset_initializes_valid_forms(
    user, cache_versions, dynamic_settings, thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_reply_thread_formset(request, thread)
    assert not formset.title
    assert formset.post
    assert not formset.invite_users


def test_get_reply_thread_formset_setups_post_form_with_attachment_uploads(
    user, cache_versions, dynamic_settings, thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_reply_thread_formset(request, thread)
    assert formset.post.show_attachments_upload


def test_get_reply_thread_formset_setups_post_form_with_attachment_upload_if_uploads_are_limited_to_threads(
    user, members_group, cache_versions, dynamic_settings, thread
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_reply_thread_formset(request, thread)
    assert formset.post.show_attachments_upload


def test_get_reply_thread_formset_setups_post_form_without_attachment_upload_if_user_has_no_permission(
    user, members_group, cache_versions, dynamic_settings, thread
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_reply_thread_formset(request, thread)
    assert not formset.post.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE)
def test_get_reply_thread_formset_setups_post_form_without_attachment_upload_if_uploads_are_disabled(
    user, cache_versions, dynamic_settings, thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_reply_thread_formset(request, thread)
    assert not formset.post.show_attachments_upload


def test_get_reply_private_thread_formset_initializes_valid_forms(
    user, cache_versions, dynamic_settings, private_thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_reply_private_thread_formset(request, private_thread)
    assert not formset.title
    assert formset.post
    assert not formset.invite_users


def test_get_reply_private_thread_formset_setups_post_form_with_attachment_uploads(
    user, cache_versions, dynamic_settings, private_thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_reply_private_thread_formset(request, private_thread)
    assert formset.post.show_attachments_upload


def test_get_reply_private_thread_formset_setups_post_form_without_attachment_upload_if_uploads_are_limited_to_threads(
    user, members_group, cache_versions, dynamic_settings, private_thread
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_reply_private_thread_formset(request, private_thread)
    assert not formset.post.show_attachments_upload


def test_get_reply_private_thread_formset_setups_post_form_without_attachment_upload_if_user_has_no_permission(
    user, members_group, cache_versions, dynamic_settings, private_thread
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_reply_private_thread_formset(request, private_thread)
    assert not formset.post.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE)
def test_get_reply_private_thread_formset_setups_post_form_without_attachment_upload_if_uploads_are_disabled(
    user, cache_versions, dynamic_settings, private_thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_reply_private_thread_formset(request, private_thread)
    assert not formset.post.show_attachments_upload


@override_dynamic_settings(allow_private_threads_attachments=False)
def test_get_reply_private_thread_formset_setups_post_form_without_attachment_upload_if_private_threads_uploads_are_disabled(
    user, cache_versions, dynamic_settings, private_thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_reply_private_thread_formset(request, private_thread)
    assert not formset.post.show_attachments_upload


def test_get_edit_thread_formset_initializes_valid_forms(
    user, cache_versions, dynamic_settings, thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_thread_formset(request, thread.first_post)
    assert formset.title
    assert formset.post
    assert not formset.invite_users


def test_get_edit_thread_formset_loads_post_attachments(
    user,
    other_user,
    cache_versions,
    dynamic_settings,
    thread,
    text_file,
    attachment_factory,
    other_thread,
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )

    attachment = attachment_factory(text_file, uploader=user, post=thread.first_post)
    second_attachment = attachment_factory(
        text_file, uploader=other_user, post=thread.first_post
    )
    attachment_factory(text_file, uploader=other_user, post=other_thread.first_post)
    attachment_factory(text_file, uploader=user)
    attachment_factory(text_file, uploader=other_user)
    attachment_factory(
        text_file, uploader=user, post=thread.first_post, is_deleted=True
    )

    formset = get_edit_thread_formset(request, thread.first_post)
    assert formset.title
    assert formset.post
    assert not formset.invite_users
    assert formset.post.attachments == [second_attachment, attachment]


def test_get_edit_thread_formset_setups_post_form_with_attachment_uploads(
    user, cache_versions, dynamic_settings, thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_thread_formset(request, thread.first_post)
    assert formset.post.show_attachments_upload


def test_get_edit_thread_formset_setups_post_form_with_attachment_upload_if_uploads_are_limited_to_threads(
    user, members_group, cache_versions, dynamic_settings, thread
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_thread_formset(request, thread.first_post)
    assert formset.post.show_attachments_upload


def test_get_edit_thread_formset_setups_post_form_without_attachment_upload_if_user_has_no_permission(
    user, members_group, cache_versions, dynamic_settings, thread
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_thread_formset(request, thread.first_post)
    assert not formset.post.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE)
def test_get_edit_thread_formset_setups_post_form_without_attachment_upload_if_uploads_are_disabled(
    user, cache_versions, dynamic_settings, thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_thread_formset(request, thread.first_post)
    assert not formset.post.show_attachments_upload


def test_get_edit_private_thread_formset_initializes_valid_forms(
    user, cache_versions, dynamic_settings, private_thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_private_thread_formset(request, private_thread.first_post)
    assert formset.title
    assert formset.post
    assert not formset.invite_users


def test_get_edit_private_thread_formset_loads_post_attachments(
    user,
    other_user,
    cache_versions,
    dynamic_settings,
    private_thread,
    text_file,
    attachment_factory,
    other_user_private_thread,
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )

    attachment = attachment_factory(
        text_file, uploader=user, post=private_thread.first_post
    )
    second_attachment = attachment_factory(
        text_file, uploader=other_user, post=private_thread.first_post
    )
    attachment_factory(
        text_file, uploader=other_user, post=other_user_private_thread.first_post
    )
    attachment_factory(text_file, uploader=user)
    attachment_factory(text_file, uploader=other_user)
    attachment_factory(
        text_file,
        uploader=user,
        post=other_user_private_thread.first_post,
        is_deleted=True,
    )

    formset = get_edit_private_thread_formset(request, private_thread.first_post)
    assert formset.title
    assert formset.post
    assert not formset.invite_users
    assert formset.post.attachments == [second_attachment, attachment]


def test_get_edit_private_thread_formset_setups_post_form_with_attachment_uploads(
    user, cache_versions, dynamic_settings, private_thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_private_thread_formset(request, private_thread.first_post)
    assert formset.post.show_attachments_upload


def test_get_edit_private_thread_formset_setups_post_form_without_attachment_upload_if_uploads_are_limited_to_threads(
    user, members_group, cache_versions, dynamic_settings, private_thread
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_private_thread_formset(request, private_thread.first_post)
    assert not formset.post.show_attachments_upload


def test_get_edit_private_thread_formset_setups_post_form_without_attachment_upload_if_user_has_no_permission(
    user, members_group, cache_versions, dynamic_settings, private_thread
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_private_thread_formset(request, private_thread.first_post)
    assert not formset.post.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE)
def test_get_edit_private_thread_formset_setups_post_form_without_attachment_upload_if_uploads_are_disabled(
    user, cache_versions, dynamic_settings, private_thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_private_thread_formset(request, private_thread.first_post)
    assert not formset.post.show_attachments_upload


@override_dynamic_settings(allow_private_threads_attachments=False)
def test_get_edit_private_thread_formset_setups_post_form_without_attachment_upload_if_private_threads_uploads_are_disabled(
    user, cache_versions, dynamic_settings, private_thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_private_thread_formset(request, private_thread.first_post)
    assert not formset.post.show_attachments_upload


def test_get_edit_thread_post_formset_initializes_valid_forms(
    user, cache_versions, dynamic_settings, thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_thread_post_formset(request, thread.first_post)
    assert not formset.title
    assert formset.post
    assert not formset.invite_users


def test_get_edit_thread_post_formset_loads_post_attachments(
    user,
    other_user,
    cache_versions,
    dynamic_settings,
    thread,
    text_file,
    attachment_factory,
    other_thread,
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )

    attachment = attachment_factory(text_file, uploader=user, post=thread.first_post)
    second_attachment = attachment_factory(
        text_file, uploader=other_user, post=thread.first_post
    )
    attachment_factory(text_file, uploader=other_user, post=other_thread.first_post)
    attachment_factory(text_file, uploader=user)
    attachment_factory(text_file, uploader=other_user)
    attachment_factory(
        text_file, uploader=user, post=thread.first_post, is_deleted=True
    )

    formset = get_edit_thread_post_formset(request, thread.first_post)
    assert not formset.title
    assert formset.post
    assert not formset.invite_users
    assert formset.post.attachments == [second_attachment, attachment]


def test_get_edit_thread_post_formset_setups_post_form_with_attachment_uploads(
    user, cache_versions, dynamic_settings, thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_thread_post_formset(request, thread.first_post)
    assert formset.post.show_attachments_upload


def test_get_edit_thread_post_formset_setups_post_form_with_attachment_upload_if_uploads_are_limited_to_threads(
    user, members_group, cache_versions, dynamic_settings, thread
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_thread_post_formset(request, thread.first_post)
    assert formset.post.show_attachments_upload


def test_get_edit_thread_post_formset_setups_post_form_without_attachment_upload_if_user_has_no_permission(
    user, members_group, cache_versions, dynamic_settings, thread
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_thread_post_formset(request, thread.first_post)
    assert not formset.post.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE)
def test_get_edit_thread_post_formset_setups_post_form_without_attachment_upload_if_uploads_are_disabled(
    user, cache_versions, dynamic_settings, thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_thread_post_formset(request, thread.first_post)
    assert not formset.post.show_attachments_upload


def test_get_edit_private_thread_post_formset_initializes_valid_forms(
    user, cache_versions, dynamic_settings, private_thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_private_thread_post_formset(request, private_thread.first_post)
    assert not formset.title
    assert formset.post
    assert not formset.invite_users


def test_get_edit_private_thread_post_formset_loads_post_attachments(
    user,
    other_user,
    cache_versions,
    dynamic_settings,
    private_thread,
    text_file,
    attachment_factory,
    other_user_private_thread,
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )

    attachment = attachment_factory(
        text_file, uploader=user, post=private_thread.first_post
    )
    second_attachment = attachment_factory(
        text_file, uploader=other_user, post=private_thread.first_post
    )
    attachment_factory(
        text_file, uploader=other_user, post=other_user_private_thread.first_post
    )
    attachment_factory(text_file, uploader=user)
    attachment_factory(text_file, uploader=other_user)
    attachment_factory(
        text_file, uploader=user, post=private_thread.first_post, is_deleted=True
    )

    formset = get_edit_private_thread_post_formset(request, private_thread.first_post)
    assert not formset.title
    assert formset.post
    assert not formset.invite_users
    assert formset.post.attachments == [second_attachment, attachment]


def test_get_edit_private_thread_post_formset_setups_post_form_with_attachment_uploads(
    user, cache_versions, dynamic_settings, private_thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_private_thread_post_formset(request, private_thread.first_post)
    assert formset.post.show_attachments_upload


def test_get_edit_private_thread_post_formset_setups_post_form_without_attachment_upload_if_uploads_are_limited_to_threads(
    user, members_group, cache_versions, dynamic_settings, private_thread
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_private_thread_post_formset(request, private_thread.first_post)
    assert not formset.post.show_attachments_upload


def test_get_edit_private_thread_post_formset_setups_post_form_without_attachment_upload_if_user_has_no_permission(
    user, members_group, cache_versions, dynamic_settings, private_thread
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_private_thread_post_formset(request, private_thread.first_post)
    assert not formset.post.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE)
def test_get_edit_private_thread_post_formset_setups_post_form_without_attachment_upload_if_uploads_are_disabled(
    user, cache_versions, dynamic_settings, private_thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_private_thread_post_formset(request, private_thread.first_post)
    assert not formset.post.show_attachments_upload


@override_dynamic_settings(allow_private_threads_attachments=False)
def test_get_edit_private_thread_post_formset_setups_post_form_without_attachment_upload_if_private_threads_uploads_are_disabled(
    user, cache_versions, dynamic_settings, private_thread
):
    request = Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )
    formset = get_edit_private_thread_post_formset(request, private_thread.first_post)
    assert not formset.post.show_attachments_upload
