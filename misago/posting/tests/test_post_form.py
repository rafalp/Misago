from unittest.mock import Mock

from ...attachments.enums import AllowedAttachments
from ...conf.test import override_dynamic_settings
from ...permissions.attachments import AttachmentsPermissions
from ..forms import PostForm


def test_post_form_sets_request(dynamic_settings):
    request = Mock(settings=dynamic_settings)
    form = PostForm(request=request)
    assert form.request is request


def test_post_form_sets_attachments(
    user, dynamic_settings, attachment_factory, text_file
):
    request = Mock(settings=dynamic_settings)
    attachments = [attachment_factory(text_file, uploader=user)]
    form = PostForm(request=request, attachments=attachments)
    assert form.attachments is attachments


def test_post_form_sets_attachments_permissions(dynamic_settings):
    request = Mock(settings=dynamic_settings)
    form = PostForm(
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=True,
            can_upload_attachments=True,
            attachment_size_limit=123,
            can_delete_own_attachments=True,
        ),
    )
    assert form.attachments_permissions.is_moderator
    assert form.attachments_permissions.can_upload_attachments
    assert form.attachments_permissions.attachment_size_limit == 123
    assert form.attachments_permissions.can_delete_own_attachments


def test_post_form_populates_attachments_with_temp_attachments_on_init(
    user, dynamic_settings, attachment_factory, text_file
):
    request = Mock(settings=dynamic_settings, user=user)
    attachment = attachment_factory(text_file, uploader=user)
    mock_data = Mock(getlist=Mock(return_value=[attachment.secret]))

    form = PostForm(
        mock_data,
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=True,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=True,
        ),
    )
    assert form.attachments == [attachment]


def test_post_form_appends_temp_attachments_to_attachments_on_init(
    user, dynamic_settings, attachment_factory, text_file, post
):
    request = Mock(settings=dynamic_settings, user=user)
    temp_attachment = attachment_factory(text_file, uploader=user)
    attachment = attachment_factory(text_file, uploader=user, post=post)
    mock_data = Mock(getlist=Mock(return_value=[temp_attachment.secret]))

    form = PostForm(
        mock_data,
        request=request,
        attachments=[attachment],
        attachments_permissions=AttachmentsPermissions(
            is_moderator=True,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=True,
        ),
    )
    assert form.attachments == [attachment, temp_attachment]


def test_post_form_doesnt_populate_attachments_with_temp_attachments_on_init_if_user_cant_upload_attachments(
    user, dynamic_settings, attachment_factory, text_file
):
    request = Mock(settings=dynamic_settings, user=user)
    attachment = attachment_factory(text_file, uploader=user)
    mock_data = Mock(getlist=Mock(return_value=[attachment.secret]))

    form = PostForm(
        mock_data,
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=True,
            can_upload_attachments=False,
            attachment_size_limit=0,
            can_delete_own_attachments=True,
        ),
    )
    assert form.attachments == []


def test_post_form_get_temp_attachments_updates_form_attachments(
    user, dynamic_settings, attachment_factory, text_file, post
):
    request = Mock(settings=dynamic_settings, user=user)
    other_attachment = attachment_factory(text_file, uploader=user, post=post)
    attachment = attachment_factory(text_file, uploader=user)

    form = PostForm(request=request, attachments=[other_attachment])
    form.get_temp_attachments([attachment.secret])
    assert form.attachments == [attachment, other_attachment]


def test_post_form_get_temp_attachments_excludes_other_users_temp_attachments(
    user, other_user, dynamic_settings, attachment_factory, text_file
):
    request = Mock(settings=dynamic_settings, user=user)
    attachment = attachment_factory(text_file, uploader=other_user)

    form = PostForm(request=request)
    form.get_temp_attachments([attachment.secret])
    assert form.attachments == []


def test_post_form_get_temp_attachments_excludes_attachments_with_posts(
    user, post, dynamic_settings, attachment_factory, text_file
):
    request = Mock(settings=dynamic_settings, user=user)
    attachment = attachment_factory(text_file, uploader=user, post=post)

    form = PostForm(request=request)
    form.get_temp_attachments([attachment.secret])
    assert form.attachments == []


def test_post_form_get_temp_attachments_excludes_deleted_temp_attachments(
    user, dynamic_settings, attachment_factory, text_file
):
    request = Mock(settings=dynamic_settings, user=user)

    attachment = attachment_factory(text_file, uploader=user)
    attachment.is_deleted = True
    attachment.save()

    form = PostForm(request=request)
    form.get_temp_attachments([attachment.secret])
    assert form.attachments == []


def test_post_form_show_attachments_is_true_if_form_has_attachments(
    user, dynamic_settings, attachment_factory, text_file, post
):
    request = Mock(settings=dynamic_settings, user=user)
    attachment = attachment_factory(text_file, uploader=user, post=post)

    form = PostForm(request=request, attachments=[attachment])
    assert form.show_attachments


def test_post_form_show_attachments_is_true_if_user_has_upload_permission(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=True,
        ),
    )
    assert form.show_attachments


def test_post_form_show_attachments_is_true_if_form_has_attachments_but_user_cant_upload(
    user, dynamic_settings, attachment_factory, text_file, post
):
    request = Mock(settings=dynamic_settings, user=user)
    attachment = attachment_factory(text_file, uploader=user, post=post)

    form = PostForm(
        request=request,
        attachments=[attachment],
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=False,
            attachment_size_limit=0,
            can_delete_own_attachments=False,
        ),
    )
    assert form.show_attachments


def test_post_form_show_attachments_is_false_if_form_has_no_attachments_and_user_cant_upload(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)

    form = PostForm(
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=False,
            attachment_size_limit=0,
            can_delete_own_attachments=False,
        ),
    )
    assert not form.show_attachments


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.ALL.value)
def test_post_form_show_attachments_upload_is_true_if_user_has_upload_permission_and_all_uploads_are_allowed(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=False,
        ),
    )
    assert form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.MEDIA.value)
def test_post_form_show_attachments_upload_is_true_if_user_has_upload_permission_and_only_media_uploads_are_allowed(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=False,
        ),
    )
    assert form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.IMAGES.value)
def test_post_form_show_attachments_upload_is_true_if_user_has_upload_permission_and_only_image_uploads_are_allowed(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=False,
        ),
    )
    assert form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_post_form_show_attachments_upload_is_false_if_user_has_upload_permission_and_image_uploads_are_disabled(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=False,
        ),
    )
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.ALL.value)
def test_post_form_show_attachments_upload_is_false_if_user_cant_upload_files_and_all_uploads_are_allowed(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=False,
            attachment_size_limit=0,
            can_delete_own_attachments=False,
        ),
    )
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.MEDIA.value)
def test_post_form_show_attachments_upload_is_false_if_user_cant_upload_files_and_only_media_uploads_are_allowed(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=False,
            attachment_size_limit=0,
            can_delete_own_attachments=False,
        ),
    )
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.IMAGES.value)
def test_post_form_show_attachments_upload_is_false_if_user_cant_upload_files_and_only_image_uploads_are_allowed(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=False,
            attachment_size_limit=0,
            can_delete_own_attachments=False,
        ),
    )
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_post_form_show_attachments_upload_is_false_if_user_cant_upload_files_and_image_uploads_are_disabled(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=False,
            attachment_size_limit=0,
            can_delete_own_attachments=False,
        ),
    )
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.ALL.value)
def test_post_form_show_attachments_upload_is_false_if_permissions_are_not_set_and_all_uploads_are_allowed(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request)
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.MEDIA.value)
def test_post_form_show_attachments_upload_is_false_if_permissions_are_not_set_and_only_media_uploads_are_allowed(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request)
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.IMAGES.value)
def test_post_form_show_attachments_upload_is_false_if_permissions_are_not_set_and_only_image_uploads_are_allowed(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request)
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_post_form_show_attachments_upload_is_false_if_permissions_are_not_set_and_image_uploads_are_disabled(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request)
    assert not form.show_attachments_upload


def test_post_form_max_attachments_returns_post_attachments_limit_setting_value(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request)
    assert form.max_attachments == dynamic_settings.post_attachments_limit


def test_post_form_attachment_size_limit_returns_size_limit_from_permissions_converted_to_bytes(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=False,
            attachment_size_limit=1234,
            can_delete_own_attachments=False,
        ),
    )
    assert form.attachment_size_limit == 1234 * 1024


def test_post_form_attachment_size_limit_returns_zero_if_permissions_are_not_set(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request)
    assert form.attachment_size_limit == 0
