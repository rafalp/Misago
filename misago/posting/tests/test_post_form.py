from unittest.mock import Mock

from django.core.files.uploadedfile import SimpleUploadedFile

from ...attachments.enums import AllowedAttachments
from ...conf.test import override_dynamic_settings
from ...permissions.attachments import AttachmentsPermissions
from ..forms import PostForm


class MockQueryDict(dict):
    def get(self, key: str, default=None):
        if key not in self:
            return default

        value = self[key]
        if isinstance(value, list):
            return value[0]

        return value

    def getlist(self, key: str, default=None):
        if key not in self:
            return default

        return list(self[key])


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


def test_post_form_populates_attachments_with_unused_attachments_on_init(
    user, dynamic_settings, attachment_factory, text_file
):
    request = Mock(settings=dynamic_settings, user=user)
    attachment = attachment_factory(text_file, uploader=user)
    data = MockQueryDict({PostForm.attachment_secret_name: [attachment.secret]})

    form = PostForm(
        data,
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=True,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=True,
        ),
    )
    assert form.attachments == [attachment]


def test_post_form_appends_unused_attachments_to_attachments_on_init(
    user, dynamic_settings, attachment_factory, text_file, post
):
    request = Mock(settings=dynamic_settings, user=user)
    unused_attachment = attachment_factory(text_file, uploader=user)
    attachment = attachment_factory(text_file, uploader=user, post=post)
    data = MockQueryDict({PostForm.attachment_secret_name: [unused_attachment.secret]})

    form = PostForm(
        data,
        request=request,
        attachments=[attachment],
        attachments_permissions=AttachmentsPermissions(
            is_moderator=True,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=True,
        ),
    )
    assert form.attachments == [attachment, unused_attachment]


def test_post_form_doesnt_populate_attachments_with_unused_attachments_on_init_if_user_cant_upload_attachments(
    user, dynamic_settings, attachment_factory, text_file
):
    request = Mock(settings=dynamic_settings, user=user)
    attachment = attachment_factory(text_file, uploader=user)
    data = MockQueryDict({PostForm.attachment_secret_name: [attachment.secret]})

    form = PostForm(
        data,
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=True,
            can_upload_attachments=False,
            attachment_size_limit=0,
            can_delete_own_attachments=True,
        ),
    )
    assert form.attachments == []


def test_post_form_get_unused_attachments_updates_form_attachments(
    user, dynamic_settings, attachment_factory, text_file, post
):
    request = Mock(settings=dynamic_settings, user=user)
    other_attachment = attachment_factory(text_file, uploader=user, post=post)
    attachment = attachment_factory(text_file, uploader=user)

    form = PostForm(request=request, attachments=[other_attachment])
    form.get_unused_attachments([attachment.secret])
    assert form.attachments == [attachment, other_attachment]


def test_post_form_get_unused_attachments_excludes_other_users_unused_attachments(
    user, other_user, dynamic_settings, attachment_factory, text_file
):
    request = Mock(settings=dynamic_settings, user=user)
    attachment = attachment_factory(text_file, uploader=other_user)

    form = PostForm(request=request)
    form.get_unused_attachments([attachment.secret])
    assert form.attachments == []


def test_post_form_get_unused_attachments_excludes_attachments_with_posts(
    user, post, dynamic_settings, attachment_factory, text_file
):
    request = Mock(settings=dynamic_settings, user=user)
    attachment = attachment_factory(text_file, uploader=user, post=post)

    form = PostForm(request=request)
    form.get_unused_attachments([attachment.secret])
    assert form.attachments == []


def test_post_form_get_unused_attachments_excludes_deleted_unused_attachments(
    user, dynamic_settings, attachment_factory, text_file
):
    request = Mock(settings=dynamic_settings, user=user)

    attachment = attachment_factory(text_file, uploader=user)
    attachment.is_deleted = True
    attachment.save()

    form = PostForm(request=request)
    form.get_unused_attachments([attachment.secret])
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


def test_post_form_includes_upload_field_if_show_attachments_upload_is_true(
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
    assert form.fields["upload"]


def test_post_form_excludes_upload_field_if_show_attachments_upload_is_false(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request)
    assert "upload" not in form.fields


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


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.ALL.value)
def test_post_form_accept_attachments_returns_all_types(user, dynamic_settings):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request)

    types = form.accept_attachments
    assert "jpeg" in types
    assert "mp4" in types
    assert "pdf" in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.MEDIA.value)
def test_post_form_accept_attachments_returns_only_media_types(user, dynamic_settings):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request)

    types = form.accept_attachments
    assert "jpeg" in types
    assert "mp4" in types
    assert "pdf" not in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.IMAGES.value)
def test_post_form_accept_attachments_returns_only_image_types(user, dynamic_settings):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request)

    types = form.accept_attachments
    assert "jpeg" in types
    assert "mp4" not in types
    assert "pdf" not in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_post_form_accept_attachments_returns_empty_str_types(user, dynamic_settings):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request)

    assert form.accept_attachments == ""


def test_post_form_attachments_media_returns_media_attachments_only(
    user, dynamic_settings, attachment_factory, image_small, text_file
):
    media_attachment = attachment_factory(image_small, uploader=user)
    file_attachment = attachment_factory(text_file, uploader=user)

    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request, attachments=[media_attachment, file_attachment])

    assert form.attachments_media == [media_attachment]


def test_post_form_attachments_other_returns_file_attachments_only(
    user, dynamic_settings, attachment_factory, image_small, text_file
):
    media_attachment = attachment_factory(image_small, uploader=user)
    file_attachment = attachment_factory(text_file, uploader=user)

    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request, attachments=[media_attachment, file_attachment])

    assert form.attachments_other == [file_attachment]


def test_post_form_sort_attachments_method_sorts_attachments_from_newest(
    user, dynamic_settings, attachment_factory, text_file
):
    first_attachment = attachment_factory(text_file, uploader=user)
    second_attachment = attachment_factory(text_file, uploader=user)

    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(request=request)
    form.attachments = [first_attachment, second_attachment]

    form.sort_attachments()
    assert form.attachments == [second_attachment, first_attachment]


def test_post_form_clean_upload_cleans_and_stores_valid_upload(user, dynamic_settings):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        MockQueryDict({"post": "Hello world!"}),
        {"upload": [SimpleUploadedFile("test.txt", b"Hello world!", "text/plain")]},
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=True,
        ),
    )

    assert form.is_valid()
    assert len(form.attachments) == 1

    attachment = form.attachments[0]
    assert attachment.filetype_id == "txt"
    assert attachment.name == "test.txt"
    assert attachment.uploader == user


def test_post_form_clean_upload_sets_error_for_invalid_upload(user, dynamic_settings):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        MockQueryDict({"post": "Hello world!"}),
        {"upload": [SimpleUploadedFile("test.txt", b"Hello world!", "text/invalid")]},
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=True,
        ),
    )

    assert not form.is_valid()
    assert not form.attachments
    assert form.errors["upload"] == ["test.txt: uploaded file type is not allowed."]


def test_post_form_clean_upload_stores_valid_uploads_on_upload_errors(
    user, dynamic_settings
):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        MockQueryDict({"post": "Hello world!"}),
        {
            "upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
                SimpleUploadedFile("invalid.txt", b"Hello world!", "text/invalid"),
            ]
        },
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=True,
        ),
    )

    assert not form.is_valid()
    assert len(form.attachments) == 1
    assert form.errors["upload"] == ["invalid.txt: uploaded file type is not allowed."]

    attachment = form.attachments[0]
    assert attachment.filetype_id == "txt"
    assert attachment.name == "test.txt"
    assert attachment.uploader == user


@override_dynamic_settings(post_attachments_limit=2)
def test_post_form_clean_upload_validates_attachments_limit(user, dynamic_settings):
    request = Mock(settings=dynamic_settings, user=user)
    form = PostForm(
        MockQueryDict({"post": "Hello world!"}),
        {
            "upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            ]
            * 3
        },
        request=request,
        attachments_permissions=AttachmentsPermissions(
            is_moderator=False,
            can_upload_attachments=True,
            attachment_size_limit=0,
            can_delete_own_attachments=True,
        ),
    )

    assert not form.is_valid()
    assert not form.attachments
    assert form.errors["upload"] == [
        "Posted message cannot have more than 2 attachments (it has 3).",
    ]
