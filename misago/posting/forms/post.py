from django import forms
from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import pgettext_lazy

from ...attachments.models import Attachment
from ...attachments.validators import validate_attachments_limit
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

    template_name = "misago/posting/post_form.html"

    post = forms.CharField(
        widget=forms.Textarea,
        error_messages={
            "required": pgettext_lazy("post validator", "Enter post's content."),
        },
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.attachments = kwargs.pop("attachments", [])
        self.attachments_permissions = kwargs.pop("attachments_permissions", None)

        super().__init__(*args, **kwargs)

        if self.show_attachments_upload:
            self.fields["upload"] = MultipleFileField(required=False)

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

        for upload in data:
            print(upload)

        return data

    def update_state(self, state: PostingState):
        state.set_post_message(self.cleaned_data["post"])


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
