from django import forms
from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import pgettext_lazy

from ...attachments.enums import (
    AllowedAttachments,
    AttachmentType,
    AttachmentTypeRestriction,
)
from ...attachments.filetypes import filetypes
from ...attachments.models import Attachment
from ...attachments.upload import handle_attachments_upload
from ...attachments.validators import validate_post_attachments_limit
from ..state import PostingState
from ..validators import validate_post
from .base import PostingForm
from .attachments import MultipleFileField


class PostForm(PostingForm):
    form_prefix = "posting-post"
    template_name = "misago/posting/post_form.html"

    upload_action = "upload_attachments"
    attachment_ids_field = "attachment_id"
    deleted_attachment_ids_field = "deleted_attachment_id"
    delete_attachment_field = "delete_attachment"

    request: HttpRequest

    attachments: list[Attachment]
    deleted_attachments: list[Attachment]
    can_upload_attachments: bool

    post = forms.CharField(
        widget=forms.Textarea,
        error_messages={
            "required": pgettext_lazy("post validator", "Enter post's content."),
        },
    )

    def __init__(self, data=None, *args, **kwargs):
        self.request = kwargs.pop("request")

        self.attachments = kwargs.pop("attachments", None) or []
        self.deleted_attachments = []
        self.can_upload_attachments = bool(kwargs.pop("can_upload_attachments", None))

        super().__init__(data, *args, **kwargs)

        if self.request.settings.post_length_max:
            self.fields["post"].max_length = self.request.settings.post_length_max

        if self.show_attachments_upload:
            self.fields["upload"] = MultipleFileField(required=False)

            if data:
                if attachments_ids := data.getlist(self.attachment_ids_field):
                    self.set_attachments(attachments_ids)

        if data and self.attachments:
            delete_attachments_ids = data.getlist(self.deleted_attachment_ids_field)
            if data.get(self.delete_attachment_field):
                delete_attachments_ids.append(data[self.delete_attachment_field])
            if delete_attachments_ids:
                self.set_deleted_attachments(delete_attachments_ids)

    @property
    def show_attachments(self) -> bool:
        return bool(self.attachments or self.show_attachments_upload)

    @property
    def show_attachments_upload(self) -> bool:
        settings = self.request.settings
        return (
            self.can_upload_attachments
            and settings.allowed_attachment_types != AllowedAttachments.NONE
        )

    @property
    def attachments_limit(self) -> int:
        return min(
            self.request.settings.post_attachments_limit,
            settings.MISAGO_POST_ATTACHMENTS_LIMIT,
        )

    @property
    def attachment_size_limit(self) -> int:
        return self.request.user_permissions.attachment_size_limit

    @property
    def accept_attachments(self) -> str:
        return self.get_accept_attachments()

    @property
    def accept_image_attachments(self) -> str:
        return self.get_accept_attachments(type_filter=AttachmentType.IMAGE)

    @property
    def accept_video_attachments(self) -> str:
        return self.get_accept_attachments(type_filter=AttachmentType.VIDEO)

    def get_accept_attachments(self, type_filter: AttachmentType | None = None) -> str:
        extensions = self.request.settings.restrict_attachments_extensions.split()
        if not extensions:
            return filetypes.get_accept_attr_str(
                self.request.settings.allowed_attachment_types,
                type_filter=type_filter,
            )

        restriction = self.request.settings.restrict_attachments_extensions_type
        if restriction == AttachmentTypeRestriction.REQUIRE:
            return filetypes.get_accept_attr_str(
                self.request.settings.allowed_attachment_types,
                require_extensions=extensions,
                type_filter=type_filter,
            )
        else:
            return filetypes.get_accept_attr_str(
                self.request.settings.allowed_attachment_types,
                disallow_extensions=extensions,
                type_filter=type_filter,
            )

    @property
    def attachments_media(self) -> list[Attachment]:
        return [
            a
            for a in self.attachments
            if a.filetype.is_media and a not in self.deleted_attachments
        ]

    @property
    def attachments_other(self) -> list[Attachment]:
        return [
            a
            for a in self.attachments
            if not a.filetype.is_media and a not in self.deleted_attachments
        ]

    def sort_attachments(self):
        self.attachments.sort(key=lambda a: a.id, reverse=True)

    def set_attachments(self, ids: list[str]):
        ids = self.clean_ids(ids)
        ids = ids.difference([a.id for a in self.attachments])

        limit = settings.MISAGO_POST_ATTACHMENTS_LIMIT - len(self.attachments)

        if ids and limit > 0:
            self.attachments.extend(
                Attachment.objects.filter(
                    id__in=ids,
                    post__isnull=True,
                    uploader=self.request.user,
                    is_deleted=False,
                ).order_by("-id")[:limit]
            )

        self.sort_attachments()

    def set_deleted_attachments(self, ids: list[str]):
        ids = self.clean_ids(ids)
        for attachment in self.attachments:
            if attachment.id in ids:
                self.deleted_attachments.append(attachment)

    def clean_ids(self, ids: list[str]) -> set[int]:
        clean_ids: set[str] = set()
        for value in ids:
            try:
                clean_value = int(value)
                if clean_value > 0:
                    clean_ids.add(clean_value)
            except (TypeError, ValueError):
                pass
        return clean_ids

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

        validate_post_attachments_limit(len(data), self.attachments_limit)
        attachments, error = handle_attachments_upload(self.request, data)

        self.attachments += attachments
        self.sort_attachments()

        if error:
            raise error

        return data

    def clean_attachments_limit(self):
        attachments_changed = not all(a.post_id for a in self.attachments)
        attachments_count = len(self.attachments) - len(self.deleted_attachments)

        if (
            self.show_attachments_upload
            and "upload" not in self.errors
            and attachments_changed
            and attachments_count > self.attachments_limit
        ):
            try:
                validate_post_attachments_limit(
                    attachments_count, self.attachments_limit
                )
            except forms.ValidationError as error:
                self.add_error("upload", error)

    def clean(self):
        cleaned_data = super().clean()

        self.clean_attachments_limit()

        return cleaned_data

    def update_state(self, state: PostingState):
        state.set_post_message(self.cleaned_data["post"])
        state.set_attachments(self.attachments)
        state.set_delete_attachments(self.deleted_attachments)

    @classmethod
    def is_request_upload(cls, request: HttpRequest) -> bool:
        return bool(
            request.method == "POST"
            and (
                request.POST.get(cls.upload_action)
                or request.POST.get(cls.delete_attachment_field)
            )
        )

    def clear_errors_in_preview(self):
        return

    def clear_errors_in_upload(self):
        self.errors.pop("post", None)


def create_post_form(
    request: HttpRequest,
    *,
    attachments: list[Attachment] | None = None,
    can_upload_attachments: bool = False,
    initial: str | None = None,
) -> PostForm:
    kwargs = {
        "request": request,
        "attachments": attachments,
        "can_upload_attachments": can_upload_attachments,
        "prefix": PostForm.form_prefix,
    }

    if request.method == "POST":
        return PostForm(request.POST, request.FILES, **kwargs)

    if initial:
        kwargs["initial"] = {"post": initial}

    return PostForm(**kwargs)
