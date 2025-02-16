from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from ...attachments.enums import AllowedAttachments, AttachmentTypeRestriction
from ...conf.test import override_dynamic_settings
from ...permissions.proxy import UserPermissionsProxy
from ..forms import PostForm


def test_post_form_sets_request(rf, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PostForm(request=request)
    assert form.request is request


def test_post_form_sets_attachments(rf, user, dynamic_settings, user_text_attachment):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    attachments = [user_text_attachment]
    form = PostForm(request=request, attachments=attachments)
    assert form.attachments == attachments


def test_post_form_sets_other_users_attachments(
    rf, user, dynamic_settings, other_user_text_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    attachments = [other_user_text_attachment]
    form = PostForm(request=request, attachments=attachments)
    assert form.attachments == attachments


def test_post_form_sets_can_upload_attachment(rf, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PostForm(
        request=request,
        can_upload_attachments=True,
    )
    assert form.can_upload_attachments


def test_post_form_sets_can_upload_attachment_as_false_by_default(rf, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PostForm(request=request)
    assert form.can_upload_attachments is False


def test_post_form_populates_attachments_with_unused_attachments_on_init(
    rf, user, dynamic_settings, user_text_attachment
):
    request = rf.post("/", {PostForm.attachment_ids_field: [user_text_attachment.id]})
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request.POST,
        request=request,
        can_upload_attachments=True,
    )
    assert form.attachments == [user_text_attachment]


def test_post_form_appends_unused_attachments_to_attachments_on_init(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    request = rf.post("/", {PostForm.attachment_ids_field: [user_image_attachment.id]})
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request.POST,
        request=request,
        attachments=[user_text_attachment],
        can_upload_attachments=True,
    )
    assert form.attachments == [user_image_attachment, user_text_attachment]


def test_post_form_doesnt_populate_attachments_with_unused_attachments_on_init_if_user_cant_upload_attachments(
    rf, user, dynamic_settings, user_text_attachment
):
    request = rf.post("/", {PostForm.attachment_ids_field: [user_text_attachment.id]})
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request.POST,
        request=request,
        can_upload_attachments=False,
    )
    assert form.attachments == []


def test_post_form_sets_deleted_attachments_on_init(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    request = rf.post(
        "/", {PostForm.deleted_attachment_ids_field: [user_text_attachment.id]}
    )
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request.POST,
        request=request,
        attachments=[user_text_attachment, user_image_attachment],
        can_upload_attachments=True,
    )
    assert form.attachments == [user_text_attachment, user_image_attachment]
    assert form.deleted_attachments == [user_text_attachment]


def test_post_form_sets_deleted_attachments_on_init_if_user_cant_upload_attachments(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    request = rf.post(
        "/", {PostForm.deleted_attachment_ids_field: [user_text_attachment.id]}
    )
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request.POST,
        request=request,
        attachments=[user_text_attachment, user_image_attachment],
        can_upload_attachments=False,
    )
    assert form.attachments == [user_text_attachment, user_image_attachment]
    assert form.deleted_attachments == [user_text_attachment]


def test_post_form_sets_deleted_attachments_on_init_from_delete_attachment_field(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    request = rf.post("/", {PostForm.delete_attachment_field: user_text_attachment.id})
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request.POST,
        request=request,
        attachments=[user_text_attachment, user_image_attachment],
        can_upload_attachments=True,
    )
    assert form.attachments == [user_text_attachment, user_image_attachment]
    assert form.deleted_attachments == [user_text_attachment]


def test_post_form_sets_deleted_attachments_on_init_from_delete_attachment_field_if_user_cant_upload_attachments(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    request = rf.post("/", {PostForm.delete_attachment_field: user_text_attachment.id})
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request.POST,
        request=request,
        attachments=[user_text_attachment, user_image_attachment],
        can_upload_attachments=False,
    )
    assert form.attachments == [user_text_attachment, user_image_attachment]
    assert form.deleted_attachments == [user_text_attachment]


def test_post_form_sets_deleted_attachments_on_init_from_both_delete_fields(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    request = rf.post(
        "/",
        {
            PostForm.delete_attachment_field: user_text_attachment.id,
            PostForm.deleted_attachment_ids_field: [user_image_attachment.id],
        },
    )
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request.POST,
        request=request,
        attachments=[user_text_attachment, user_image_attachment],
        can_upload_attachments=True,
    )
    assert form.attachments == [user_text_attachment, user_image_attachment]
    assert form.deleted_attachments == [user_text_attachment, user_image_attachment]


def test_post_form_set_attachments_sets_form_attachments(
    rf, user, dynamic_settings, user_text_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    form.set_attachments([user_text_attachment.id])
    assert form.attachments == [user_text_attachment]


def test_post_form_set_attachments_supports_strings(
    rf, user, dynamic_settings, user_text_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    form.set_attachments([str(user_text_attachment.id)])
    assert form.attachments == [user_text_attachment]


def test_post_form_set_attachments_handles_duplicates(
    rf, user, dynamic_settings, user_text_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    form.set_attachments([user_text_attachment.id, user_text_attachment.id])
    assert form.attachments == [user_text_attachment]


def test_post_form_set_attachments_handles_invalid_ids(rf, user, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    form.set_attachments(["invalid"])
    assert form.attachments == []


def test_post_form_set_attachments_handles_negative_ids(rf, user, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    form.set_attachments([-10])
    assert form.attachments == []


def test_post_form_set_attachments_updates_form_attachments(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request, attachments=[user_text_attachment])
    form.set_attachments([user_image_attachment.id])
    assert form.attachments == [user_image_attachment, user_text_attachment]


def test_post_form_set_attachments_excludes_other_users_unused_attachments(
    rf, user, dynamic_settings, other_user_text_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    form.set_attachments([other_user_text_attachment.id])
    assert form.attachments == []


def test_post_form_set_attachments_excludes_attachments_with_posts(
    rf, user, dynamic_settings, user_text_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    form.set_attachments([user_text_attachment.id])
    assert form.attachments == []


def test_post_form_set_attachments_excludes_deleted_unused_attachments(
    rf, user, dynamic_settings, user_text_attachment
):
    user_text_attachment.is_deleted = True
    user_text_attachment.save()

    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    form.set_attachments([user_text_attachment.id])
    assert form.attachments == []


@override_settings(MISAGO_POST_ATTACHMENTS_LIMIT=1)
def test_post_form_set_attachments_excludes_unused_attachments_over_hard_limit(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    form.set_attachments([user_text_attachment.id, user_image_attachment.id])
    assert form.attachments == [user_image_attachment]


@override_settings(MISAGO_POST_ATTACHMENTS_LIMIT=1)
def test_post_form_set_attachments_counts_existing_attachments_to_hard_limit(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request, attachments=[user_text_attachment])
    form.set_attachments([user_image_attachment.id])
    assert form.attachments == [user_text_attachment]


def test_post_form_set_deleted_attachments_sets_existing_attachment_as_deleted(
    rf, user, dynamic_settings, user_text_attachment
):
    user_text_attachment.is_deleted = True
    user_text_attachment.save()

    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request, attachments=[user_text_attachment])
    form.set_deleted_attachments([user_text_attachment.id])
    assert form.attachments == [user_text_attachment]
    assert form.deleted_attachments == [user_text_attachment]


def test_post_form_set_deleted_attachments_excludes_other_attachments(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment
):
    user_text_attachment.is_deleted = True
    user_text_attachment.save()

    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        attachments=[user_image_attachment, user_text_attachment],
    )
    form.set_deleted_attachments([user_text_attachment.id])
    assert form.attachments == [user_image_attachment, user_text_attachment]
    assert form.deleted_attachments == [user_text_attachment]


def test_post_form_set_deleted_attachments_supports_strings(
    rf, user, dynamic_settings, user_text_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request, attachments=[user_text_attachment])
    form.set_deleted_attachments([str(user_text_attachment.id)])
    assert form.attachments == [user_text_attachment]
    assert form.deleted_attachments == [user_text_attachment]


def test_post_form_set_deleted_attachments_handles_duplicates(
    rf, user, dynamic_settings, user_text_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request, attachments=[user_text_attachment])
    form.set_deleted_attachments([user_text_attachment.id, user_text_attachment.id])
    assert form.attachments == [user_text_attachment]
    assert form.deleted_attachments == [user_text_attachment]


def test_post_form_set_deleted_attachments_handles_invalid_ids(
    rf, user, dynamic_settings, user_text_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request, attachments=[user_text_attachment])
    form.set_deleted_attachments(["invalid"])
    assert form.attachments == [user_text_attachment]
    assert form.deleted_attachments == []


def test_post_form_set_deleted_attachments_handles_negative_ids(
    rf, user, dynamic_settings, user_text_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request, attachments=[user_text_attachment])
    form.set_deleted_attachments([-10])
    assert form.attachments == [user_text_attachment]
    assert form.deleted_attachments == []


def test_post_form_set_deleted_attachments_handles_non_existing_ids(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request, attachments=[user_text_attachment])
    form.set_deleted_attachments([user_image_attachment.id])
    assert form.attachments == [user_text_attachment]
    assert form.deleted_attachments == []


def test_post_form_show_attachments_is_true_if_form_has_attachments(
    rf, user, dynamic_settings, user_text_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request, attachments=[user_text_attachment])
    assert form.show_attachments


def test_post_form_show_attachments_is_true_if_user_has_upload_permission(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        can_upload_attachments=True,
    )
    assert form.show_attachments


def test_post_form_show_attachments_is_true_if_form_has_attachments_but_user_cant_upload(
    rf, user, dynamic_settings, user_text_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        attachments=[user_text_attachment],
        can_upload_attachments=False,
    )
    assert form.show_attachments


def test_post_form_show_attachments_is_false_if_form_has_no_attachments_and_user_cant_upload(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        can_upload_attachments=False,
    )
    assert not form.show_attachments


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.ALL.value)
def test_post_form_show_attachments_upload_is_true_if_user_has_upload_permission_and_all_uploads_are_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        can_upload_attachments=True,
    )
    assert form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.MEDIA.value)
def test_post_form_show_attachments_upload_is_true_if_user_has_upload_permission_and_only_media_uploads_are_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        can_upload_attachments=True,
    )
    assert form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.IMAGES.value)
def test_post_form_show_attachments_upload_is_true_if_user_has_upload_permission_and_only_image_uploads_are_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        can_upload_attachments=True,
    )
    assert form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_post_form_show_attachments_upload_is_false_if_user_has_upload_permission_and_image_uploads_are_disabled(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        can_upload_attachments=True,
    )
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.ALL.value)
def test_post_form_show_attachments_upload_is_false_if_user_cant_upload_files_and_all_uploads_are_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        can_upload_attachments=False,
    )
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.MEDIA.value)
def test_post_form_show_attachments_upload_is_false_if_user_cant_upload_files_and_only_media_uploads_are_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        can_upload_attachments=False,
    )
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.IMAGES.value)
def test_post_form_show_attachments_upload_is_false_if_user_cant_upload_files_and_only_image_uploads_are_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        can_upload_attachments=False,
    )
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_post_form_show_attachments_upload_is_false_if_user_cant_upload_files_and_image_uploads_are_disabled(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        can_upload_attachments=False,
    )
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.ALL.value)
def test_post_form_show_attachments_upload_is_false_if_permissions_are_not_set_and_all_uploads_are_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.MEDIA.value)
def test_post_form_show_attachments_upload_is_false_if_permissions_are_not_set_and_only_media_uploads_are_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.IMAGES.value)
def test_post_form_show_attachments_upload_is_false_if_permissions_are_not_set_and_only_image_uploads_are_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    assert not form.show_attachments_upload


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_post_form_show_attachments_upload_is_false_if_permissions_are_not_set_and_image_uploads_are_disabled(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    assert not form.show_attachments_upload


def test_post_form_includes_upload_field_if_show_attachments_upload_is_true(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(
        request=request,
        can_upload_attachments=True,
    )
    assert form.fields["upload"]


def test_post_form_excludes_upload_field_if_show_attachments_upload_is_false(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    assert "upload" not in form.fields


def test_post_form_attachments_limit_returns_post_attachments_limit_setting_value(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    assert form.attachments_limit == dynamic_settings.post_attachments_limit


@override_dynamic_settings(post_attachments_limit=50)
@override_settings(MISAGO_POST_ATTACHMENTS_LIMIT=20)
def test_post_form_attachments_limit_returns_hard_post_attachments_limit_setting_value_if_lower(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    assert form.attachments_limit == 20


def test_post_form_attachment_size_limit_returns_size_limit_from_user_permissions(
    rf, user, members_group, dynamic_settings, cache_versions
):
    members_group.attachment_size_limit = 42
    members_group.save()

    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    form = PostForm(
        request=request,
        can_upload_attachments=False,
    )
    assert form.attachment_size_limit == members_group.attachment_size_limit * 1024


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.ALL.value)
def test_post_form_accept_attachments_returns_all_types(rf, user, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_attachments
    assert "jpeg" in types
    assert "mp4" in types
    assert "pdf" in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.MEDIA.value)
def test_post_form_accept_attachments_returns_only_media_types(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_attachments
    assert "jpeg" in types
    assert "mp4" in types
    assert "pdf" not in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.IMAGES.value)
def test_post_form_accept_attachments_returns_only_image_types(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_attachments
    assert "jpeg" in types
    assert "mp4" not in types
    assert "pdf" not in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_post_form_accept_attachments_returns_empty_str_types(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    assert form.accept_attachments == ""


@override_dynamic_settings(
    allowed_attachment_types=AllowedAttachments.IMAGES.value,
    restrict_attachments_extensions="jpg png",
    restrict_attachments_extensions_type=AttachmentTypeRestriction.REQUIRE.value,
)
def test_post_form_accept_attachments_returns_only_required_types(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_attachments
    assert "jpg" in types
    assert "png" in types
    assert "jpeg" not in types
    assert "gif" not in types
    assert "mp4" not in types
    assert "pdf" not in types


@override_dynamic_settings(
    allowed_attachment_types=AllowedAttachments.IMAGES.value,
    restrict_attachments_extensions="jpg gif",
    restrict_attachments_extensions_type=AttachmentTypeRestriction.DISALLOW.value,
)
def test_post_form_accept_attachments_excludes_disallowed_types(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_attachments
    assert "jpeg" in types
    assert "png" in types
    assert "jpg" not in types
    assert "gif" not in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.ALL.value)
def test_post_form_accept_image_attachments_returns_all_image_types(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_image_attachments
    assert "jpeg" in types
    assert "mp4" not in types
    assert "pdf" not in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.MEDIA.value)
def test_post_form_accept_image_attachments_returns_all_image_types_if_media_is_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_image_attachments
    assert "jpeg" in types
    assert "mp4" not in types
    assert "pdf" not in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.IMAGES.value)
def test_post_form_accept_image_attachments_returns_all_image_types_if_images_is_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_image_attachments
    assert "jpeg" in types
    assert "mp4" not in types
    assert "pdf" not in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_post_form_accept_image_attachments_returns_empty_str_if_nothing_is_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    assert not form.accept_image_attachments


@override_dynamic_settings(
    allowed_attachment_types=AllowedAttachments.IMAGES.value,
    restrict_attachments_extensions="jpg png",
    restrict_attachments_extensions_type=AttachmentTypeRestriction.REQUIRE.value,
)
def test_post_form_accept_image_attachments_returns_only_required_types(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_image_attachments
    assert "jpg" in types
    assert "png" in types
    assert "jpeg" not in types
    assert "gif" not in types
    assert "mp4" not in types
    assert "pdf" not in types


@override_dynamic_settings(
    allowed_attachment_types=AllowedAttachments.IMAGES.value,
    restrict_attachments_extensions="jpg gif",
    restrict_attachments_extensions_type=AttachmentTypeRestriction.DISALLOW.value,
)
def test_post_form_accept_image_attachments_excludes_disallowed_types(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_image_attachments
    assert "jpeg" in types
    assert "png" in types
    assert "jpg" not in types
    assert "gif" not in types
    assert "mp4" not in types
    assert "pdf" not in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.ALL.value)
def test_post_form_accept_video_attachments_returns_all_video_types(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_video_attachments
    assert "mp4" in types
    assert "jpeg" not in types
    assert "pdf" not in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.MEDIA.value)
def test_post_form_accept_video_attachments_returns_all_video_types_if_media_is_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_video_attachments
    assert "mp4" in types
    assert "jpeg" not in types
    assert "pdf" not in types


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.IMAGES.value)
def test_post_form_accept_video_attachments_returns_empty_str_if_only_images_are_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    assert not form.accept_video_attachments


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_post_form_accept_video_attachments_returns_empty_str_if_nothing_is_allowed(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    assert not form.accept_video_attachments


@override_dynamic_settings(
    restrict_attachments_extensions="mp4",
    restrict_attachments_extensions_type=AttachmentTypeRestriction.REQUIRE.value,
)
def test_post_form_accept_video_attachments_returns_only_required_types(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_video_attachments
    assert "mp4" in types
    assert "webm" not in types
    assert "jpg" not in types
    assert "gif" not in types
    assert "pdf" not in types


@override_dynamic_settings(
    restrict_attachments_extensions="mp4",
    restrict_attachments_extensions_type=AttachmentTypeRestriction.DISALLOW.value,
)
def test_post_form_accept_video_attachments_excludes_disallowed_types(
    rf, user, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)

    types = form.accept_video_attachments
    assert "webm" in types
    assert "mp4" not in types
    assert "jpg" not in types
    assert "gif" not in types
    assert "pdf" not in types


def test_post_form_attachments_media_returns_media_attachments_only(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment
):
    media_attachment = user_image_attachment
    file_attachment = user_text_attachment

    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request, attachments=[media_attachment, file_attachment])

    assert form.attachments_media == [media_attachment]


def test_post_form_attachments_other_returns_file_attachments_only(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment
):
    media_attachment = user_image_attachment
    file_attachment = user_text_attachment

    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request, attachments=[media_attachment, file_attachment])

    assert form.attachments_other == [file_attachment]


def test_post_form_sort_attachments_method_sorts_attachments_from_newest(
    rf, user, dynamic_settings, user_text_attachment, user_image_attachment
):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user = user

    form = PostForm(request=request)
    form.attachments = [user_text_attachment, user_image_attachment]

    form.sort_attachments()
    assert form.attachments == [user_image_attachment, user_text_attachment]


@override_dynamic_settings(post_attachments_limit=2)
def test_post_form_clean_upload_validates_attachments_limit(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post(
        "/",
        {
            "post": "Hello world!",
            "upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
                SimpleUploadedFile("test2.txt", b"Hello world!", "text/plain"),
                SimpleUploadedFile("test3.txt", b"Hello world!", "text/plain"),
            ],
        },
    )
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    form = PostForm(
        request.POST,
        request.FILES,
        request=request,
        can_upload_attachments=True,
    )

    assert not form.is_valid()
    assert not form.attachments
    assert form.errors["upload"] == [
        "Posted message cannot have more than 2 attachments (it has 3).",
    ]


def test_post_form_clean_upload_cleans_and_stores_valid_upload(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post(
        "/",
        {
            "post": "Hello world!",
            "upload": [SimpleUploadedFile("test.txt", b"Hello world!", "text/plain")],
        },
    )
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    form = PostForm(
        request.POST,
        request.FILES,
        request=request,
        can_upload_attachments=True,
    )

    assert form.is_valid()
    assert len(form.attachments) == 1

    attachment = form.attachments[0]
    assert attachment.filetype_id == "txt"
    assert attachment.name == "test.txt"
    assert attachment.uploader == user


def test_post_form_clean_upload_validates_uploaded_files(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post(
        "/",
        {
            "post": "Hello world!",
            "upload": [SimpleUploadedFile("test.txt", b"Hello world!", "text/invalid")],
        },
    )
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    form = PostForm(
        request.POST,
        request.FILES,
        request=request,
        can_upload_attachments=True,
    )

    assert not form.is_valid()
    assert not form.attachments
    assert form.errors["upload"] == ["test.txt: uploaded file type is not allowed."]


@override_dynamic_settings(post_attachments_limit=1)
def test_post_form_clean_validates_attachments_limit(
    rf,
    user,
    dynamic_settings,
    cache_versions,
    user_text_attachment,
    user_image_attachment,
):
    request = rf.post(
        "/",
        {
            "post": "Hello world!",
            PostForm.attachment_ids_field: [
                user_text_attachment.id,
                user_image_attachment.id,
            ],
        },
    )
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    form = PostForm(
        request.POST,
        request=request,
        can_upload_attachments=True,
    )

    assert not form.is_valid()
    assert form.attachments == [user_image_attachment, user_text_attachment]
    assert form.errors["upload"] == [
        "Posted message cannot have more than 1 attachment (it has 2).",
    ]


@override_dynamic_settings(post_attachments_limit=1)
def test_post_form_clean_skips_attachments_limit_validation_all_attachments_are_used(
    rf,
    user,
    dynamic_settings,
    cache_versions,
    user_text_attachment,
    user_image_attachment,
    post,
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    user_image_attachment.associate_with_post(post)
    user_image_attachment.save()

    request = rf.post(
        "/",
        {
            "post": "Hello world!",
            PostForm.attachment_ids_field: [
                user_text_attachment.id,
                user_image_attachment.id,
            ],
        },
    )
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    form = PostForm(
        request.POST,
        request=request,
        attachments=[user_image_attachment, user_text_attachment],
        can_upload_attachments=True,
    )

    assert form.is_valid()
    assert form.attachments == [user_image_attachment, user_text_attachment]


@override_dynamic_settings(post_attachments_limit=1)
def test_post_form_clean_subtracts_deleted_attachments_from_limit(
    rf,
    user,
    dynamic_settings,
    cache_versions,
    user_text_attachment,
    user_image_attachment,
):
    request = rf.post(
        "/",
        {
            "post": "Hello world!",
            PostForm.attachment_ids_field: [
                user_text_attachment.id,
                user_image_attachment.id,
            ],
            PostForm.deleted_attachment_ids_field: [
                user_image_attachment.id,
            ],
        },
    )
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    form = PostForm(
        request.POST,
        request=request,
        can_upload_attachments=True,
    )

    assert form.is_valid()
    assert form.attachments == [user_image_attachment, user_text_attachment]
    assert form.deleted_attachments == [user_image_attachment]


def test_post_form_is_request_upload_returns_false_for_get_request(rf):
    request = rf.get("/")
    assert not PostForm.is_request_upload(request)


def test_post_form_is_request_upload_returns_false_for_regular_post_request(rf):
    request = rf.post("/", {})
    assert not PostForm.is_request_upload(request)


def test_post_form_is_request_upload_returns_true_if_upload_button_was_clicked(rf):
    request = rf.post("/", {PostForm.upload_action: "1"})
    assert PostForm.is_request_upload(request)


def test_post_form_is_request_upload_returns_true_if_delete_attachment_button_was_clicked(
    rf,
):
    request = rf.post("/", {PostForm.delete_attachment_field: "1"})
    assert PostForm.is_request_upload(request)
