from django import forms
from django.http import HttpRequest
from django.utils.translation import pgettext_lazy

from ...attachments.enums import AllowedAttachments, AttachmentTypeRestriction
from ...attachments.filetypes import filetypes
from ...attachments.models import Attachment
from ...attachments.upload import store_uploaded_file
from ...attachments.validators import (
    get_attachments_storage_constraints,
    validate_post_attachments_limit,
    validate_uploaded_file,
    validate_uploaded_file_extension,
)
from ...permissions.attachments import AttachmentsPermissions
from ..state import PostingState
from ..validators import validate_post
from .base import PostingForm
from .attachments import MultipleFileField


class PostForm(PostingForm):
    form_prefix = "posting-post"
    template_name = "misago/posting/post_form.html"
    attachment_secret_name = "attachment_secret"

    request: HttpRequest
    attachments: list[Attachment]
    attachments_permissions: AttachmentsPermissions | None

    post = forms.CharField(
        widget=forms.Textarea,
        error_messages={
            "required": pgettext_lazy("post validator", "Enter post's content."),
        },
    )

    def __init__(self, data=None, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.attachments = kwargs.pop("attachments", None) or []
        self.attachments_permissions = kwargs.pop("attachments_permissions", None)

        super().__init__(data, *args, **kwargs)

        if self.show_attachments_upload:
            self.fields["upload"] = MultipleFileField(required=False)

            if data:
                if attachments_secrets := data.getlist(self.attachment_secret_name):
                    self.get_unused_attachments(attachments_secrets)

    @property
    def show_attachments(self) -> bool:
        return bool(self.attachments or self.show_attachments_upload)

    @property
    def show_attachments_upload(self) -> bool:
        permissions = self.attachments_permissions
        settings = self.request.settings

        return (
            permissions
            and permissions.can_upload_attachments
            and settings.allowed_attachment_types != AllowedAttachments.NONE
        )

    @property
    def max_attachments(self) -> int:
        return self.request.settings.post_attachments_limit

    @property
    def attachment_size_limit(self) -> int:
        if not self.attachments_permissions:
            return 0

        return self.attachments_permissions.attachment_size_limit

    @property
    def accept_attachments(self) -> str:
        extensions = self.request.settings.restrict_attachments_extensions.split()
        if not extensions:
            return filetypes.get_accept_attr_str(
                self.request.settings.allowed_attachment_types
            )

        restriction = self.request.settings.restrict_attachments_extensions_type
        if restriction == AttachmentTypeRestriction.REQUIRE:
            return filetypes.get_accept_attr_str(
                self.request.settings.allowed_attachment_types,
                require_extensions=extensions,
            )
        else:
            return filetypes.get_accept_attr_str(
                self.request.settings.allowed_attachment_types,
                disallow_extensions=extensions,
            )

    @property
    def attachments_media(self) -> list[Attachment]:
        return [a for a in self.attachments if a.filetype.is_media]

    @property
    def attachments_other(self) -> list[Attachment]:
        return [a for a in self.attachments if not a.filetype.is_media]

    def sort_attachments(self):
        self.attachments.sort(key=lambda a: a.id, reverse=True)

    def get_unused_attachments(self, secrets: list[str]):
        clean_secrets: set[str] = set(s.strip() for s in secrets if s.strip())
        if clean_secrets:
            self.attachments.extend(
                Attachment.objects.filter(
                    post__isnull=True,
                    uploader=self.request.user,
                    secret__in=clean_secrets,
                    is_deleted=False,
                )
            )

        self.sort_attachments()

    def clean_post(self):
        data = self.cleaned_data["post"]
        validate_post(
            data,
            self.request.settings.post_length_min,
            self.request.settings.post_length_max,
            request=self.request,
        )
        return data

    def clean_upload(self):
        data = self.cleaned_data["upload"]

        validate_post_attachments_limit(len(data), self.max_attachments)

        storage_constraints = get_attachments_storage_constraints(
            self.request.settings.unused_attachments_storage_limit,
            self.request.user_permissions,
        )

        extensions = self.request.settings.restrict_attachments_extensions.split()
        extensions_restriction = (
            self.request.settings.restrict_attachments_extensions_type
        )

        errors: list[forms.ValidationError] = []
        for upload in data:
            try:
                filetype = validate_uploaded_file(
                    upload,
                    allowed_attachments=self.request.settings.allowed_attachment_types,
                    max_size=self.attachment_size_limit,
                    **storage_constraints,
                )

                if extensions:
                    validate_uploaded_file_extension(
                        upload, extensions_restriction, extensions
                    )

                attachment = store_uploaded_file(self.request, upload, filetype)
                self.attachments.append(attachment)

                attachment_size = attachment.size + attachment.thumbnail_size
                storage_constraints["storage_left"] = max(
                    storage_constraints["storage_left"] - attachment_size, 0
                )
            except forms.ValidationError as error:
                errors.append(error)

        self.sort_attachments()

        if errors:
            raise forms.ValidationError(message=errors)

        return data

    def get_attachment_storage_constraints(self) -> dict:
        pass

    def update_state(self, state: PostingState):
        state.set_post_message(self.cleaned_data["post"])
        state.set_attachments(self.attachments)

    def clear_errors_in_preview(self):
        return

    def clear_errors_in_upload(self):
        self.errors.pop("post", None)


def create_post_form(
    request: HttpRequest,
    *,
    attachments: list[Attachment] | None = None,
    attachments_permissions: AttachmentsPermissions | None = None,
    initial: str | None = None,
) -> PostForm:
    kwargs = {
        "request": request,
        "attachments": attachments,
        "attachments_permissions": attachments_permissions,
        "prefix": PostForm.form_prefix,
    }

    if request.method == "POST":
        return PostForm(request.POST, request.FILES, **kwargs)

    if initial:
        kwargs["initial"] = {"post": initial}

    return PostForm(**kwargs)
