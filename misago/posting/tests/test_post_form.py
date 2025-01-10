from unittest.mock import Mock

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
