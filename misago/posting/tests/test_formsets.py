from unittest.mock import Mock

import pytest
from django.http import HttpRequest

from ...attachments.enums import AllowedAttachments
from ...conf.test import override_dynamic_settings
from ...permissions.enums import CanUploadAttachments
from ...permissions.proxy import UserPermissionsProxy
from ..forms import PostForm, PostingForm
from ..formsets import (
    PostingFormset,
    TabbedPostingFormset,
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


def test_tabbed_posting_formset_add_tab_adds_new_tab():
    formset = TabbedPostingFormset()
    tab = formset.add_tab("test", "Test tab")
    assert formset.get_tabs() == [tab]


def test_tabbed_posting_formset_add_tab_after_adds_new_tab_after_other_one():
    formset = TabbedPostingFormset()
    tab1 = formset.add_tab("apple", "Apple")
    tab2 = formset.add_tab("orange", "Orange")
    tab3 = formset.add_tab_after("apple", "watermelon", "Watermelon")
    assert formset.get_tabs() == [tab1, tab3, tab2]


def test_tabbed_posting_formset_add_tab_after_raises_value_error_if_tab_doesnt_exist():
    formset = TabbedPostingFormset()

    with pytest.raises(ValueError) as exc_info:
        formset.add_tab_after("apple", "watermelon", "Watermelon")

    assert str(exc_info.value) == "Formset does not contain a tab with ID 'apple'."


def test_tabbed_posting_formset_add_tab_before_adds_new_tab_before_other_one():
    formset = TabbedPostingFormset()
    tab1 = formset.add_tab("apple", "Apple")
    tab2 = formset.add_tab("orange", "Orange")
    tab3 = formset.add_tab_before("orange", "watermelon", "Watermelon")
    assert formset.get_tabs() == [tab1, tab3, tab2]


def test_tabbed_posting_formset_add_tab_before_raises_value_error_if_tab_doesnt_exist():
    formset = TabbedPostingFormset()

    with pytest.raises(ValueError) as exc_info:
        formset.add_tab_before("orange", "watermelon", "Watermelon")

    assert str(exc_info.value) == "Formset does not contain a tab with ID 'orange'."


def test_tabbed_posting_formset_add_form_adds_form_to_a_tab():
    formset = TabbedPostingFormset()
    tab = formset.add_tab("test", "Test")
    form = formset.add_form("test", UploadForm(prefix="upload"))
    assert formset.get_tabs() == [tab]
    assert tab.get_forms() == [form]


def test_tabbed_posting_formset_add_form_raises_value_error_if_tab_is_invalid():
    formset = TabbedPostingFormset()

    with pytest.raises(ValueError) as exc_info:
        formset.add_form("invalid", UploadForm(prefix="upload"))

    assert str(exc_info.value) == "Formset does not contain a tab with ID 'invalid'."


def test_tabbed_posting_formset_add_form_after_adds_form_after_other_one():
    formset = TabbedPostingFormset()
    tab = formset.add_tab("test", "Test")
    form1 = formset.add_form("test", UploadForm(prefix="apple"))
    form2 = formset.add_form("test", UploadForm(prefix="orange"))
    form3 = formset.add_form_after("test", "apple", UploadForm(prefix="watermelon"))
    assert formset.get_tabs() == [tab]
    assert tab.get_forms() == [form1, form3, form2]


def test_tabbed_posting_formset_add_form_after_raises_value_error_if_tab_doesnt_exist():
    formset = TabbedPostingFormset()

    with pytest.raises(ValueError) as exc_info:
        formset.add_form_after("invalid", "apple", UploadForm(prefix="watermelon"))

    assert str(exc_info.value) == "Formset does not contain a tab with ID 'invalid'."


def test_tabbed_posting_formset_add_form_before_adds_form_before_other_one():
    formset = TabbedPostingFormset()
    tab = formset.add_tab("test", "Test")
    form1 = formset.add_form("test", UploadForm(prefix="apple"))
    form2 = formset.add_form("test", UploadForm(prefix="orange"))
    form3 = formset.add_form_before("test", "orange", UploadForm(prefix="watermelon"))
    assert formset.get_tabs() == [tab]
    assert tab.get_forms() == [form1, form3, form2]


def test_tabbed_posting_formset_add_form_before_raises_value_error_if_tab_doesnt_exist():
    formset = TabbedPostingFormset()

    with pytest.raises(ValueError) as exc_info:
        formset.add_form_before("invalid", "apple", UploadForm(prefix="watermelon"))

    assert str(exc_info.value) == "Formset does not contain a tab with ID 'invalid'."


def test_tabbed_posting_formset_is_request_preview_method_returns_false_for_not_post_request(
    rf,
):
    request = rf.get("/")
    formset = TabbedPostingFormset()
    assert not formset.is_request_preview(request)


def test_tabbed_posting_formset_is_request_preview_method_returns_false_for_post_request_without_preview(
    rf,
):
    request = rf.post("/")
    formset = TabbedPostingFormset()
    assert not formset.is_request_preview(request)


def test_tabbed_posting_formset_is_request_preview_method_returns_true_for_post_request(
    rf,
):
    request = rf.post("/", {TabbedPostingFormset.preview_action: "1"})
    formset = TabbedPostingFormset()
    assert formset.is_request_preview(request)


def test_tabbed_posting_formset_is_request_upload_method_returns_false_for_not_post_request(
    rf,
):
    request = rf.get("/")
    formset = TabbedPostingFormset()
    assert not formset.is_request_upload(request)


class UploadForm(PostingForm):
    def is_request_upload(self, request: HttpRequest) -> bool:
        return PostForm.is_request_upload(request)


def test_tabbed_posting_formset_is_request_upload_method_returns_false_for_post_request_without_upload(
    rf,
):
    request = rf.post("/")
    formset = TabbedPostingFormset()
    formset.add_tab("test", "Test")
    formset.add_form("test", UploadForm(prefix="test"))

    assert not formset.is_request_upload(request)


def test_tabbed_posting_formset_is_request_upload_method_returns_true_for_post_request_with_upload(
    rf,
):
    request = rf.post("/", {PostForm.upload_action: "1"})
    formset = TabbedPostingFormset()
    formset.add_tab("test", "Test")
    formset.add_form("test", UploadForm(prefix="test"))

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
