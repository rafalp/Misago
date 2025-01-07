from django import forms
from django.http import HttpRequest
from django.utils.translation import pgettext_lazy

from ...attachments.filetypes import filetypes
from ...attachments.models import Attachment
from ...attachments.store import store_attachment_file
from ...attachments.validators import (
    validate_attachments_limit,
    validate_uploaded_file,
)
from ...permissions.attachments import AttachmentPermissions
from ..state import PostingState
from ..validators import validate_post
from .base import PostingForm
from .attachments import MultipleFileField

PREFIX = "posting-post"


class PostForm(PostingForm):
    request: HttpRequest
    attachments: list[Attachment]
    attachments_permissions: AttachmentPermissions | None
    attachment_secret_name = "attachment_secret"

    template_name = "misago/posting/post_form.html"

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
                self.get_temp_attachments(attachments_secrets)

    @property
    def show_attachments(self) -> bool:
        if self.attachments:
            return True

        return self.show_attachments_upload

    @property
    def show_attachments_upload(self) -> bool:
        return (
            self.attachments_permissions
            and self.attachments_permissions.can_upload_attachments
        )

    @property
    def max_attachments(self) -> int:
        return self.request.settings.post_attachments_limit

    @property
    def attachment_size_limit(self) -> int:
        if not self.attachments_permissions:
            return 0

        # Return KB permission size in bytes
        return self.attachments_permissions.attachment_size_limit * 1024

    @property
    def accept_attachments(self) -> str:
        return filetypes.get_accept_attr_str()

    @property
    def attachments_media(self) -> list[Attachment]:
        return [a for a in self.attachments if a.is_image or a.is_video]

    @property
    def attachments_other(self) -> list[Attachment]:
        return [a for a in self.attachments if not (a.is_image or a.is_video)]

    def sort_attachments(self):
        self.attachments.sort(key=lambda a: a.id, reverse=True)

    def get_temp_attachments(self, secrets: list[str]):
        clean_secrets: set[str] = set(s.strip() for s in secrets if s.strip())
        if clean_secrets:
            self.attachments.extend(
                Attachment.objects.filter(
                    post__isnull=True,
                    uploader=self.request.user,
                    secret__in=clean_secrets,
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

        validate_attachments_limit(len(data), self.max_attachments)

        errors: list[forms.ValidationError] = []
        for upload in data:
            try:
                filetype = validate_uploaded_file(
                    upload, max_size=self.attachment_size_limit
                )
                self.attachments.append(
                    store_attachment_file(self.request, upload, filetype)
                )
            except forms.ValidationError as error:
                errors.append(error)

        self.sort_attachments()

        if errors:
            raise forms.ValidationError(message=errors)

        return data

    def update_state(self, state: PostingState):
        state.set_post_message(self.cleaned_data["post"])
        state.set_attachments(self.attachments)


def create_post_form(
    request: HttpRequest,
    *,
    attachments: list[Attachment] | None = None,
    attachments_permissions: AttachmentPermissions | None = None,
    initial: str | None = None,
) -> PostForm:
    kwargs = {
        "request": request,
        "attachments": attachments,
        "attachments_permissions": attachments_permissions,
        "prefix": PREFIX,
    }

    if request.method == "POST":
        return PostForm(request.POST, request.FILES, **kwargs)

    if initial:
        kwargs["initial"] = {"post": initial}

    return PostForm(**kwargs)
