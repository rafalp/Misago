from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.template.defaultfilters import filesizeformat
from django.utils.translation import npgettext, pgettext

from .enums import AllowedAttachments
from .filetypes import AttachmentFileType, filetypes


def validate_attachments_limit(value: int, limit_value: int):
    if value > limit_value:
        raise ValidationError(
            message=npgettext(
                "attachments limit validator",
                "Posted message cannot have more than %(limit_value)s attachment (it has %(show_value)s).",
                "Posted message cannot have more than %(limit_value)s attachments (it has %(show_value)s).",
                limit_value,
            ),
            code="attachments_limit",
            params={
                "limit_value": limit_value,
                "show_value": value,
            },
        )


def validate_uploaded_file(
    file: UploadedFile,
    *,
    max_size: int,
    allowed_attachments: AllowedAttachments | str,
) -> AttachmentFileType:
    filetype = filetypes.match_filetype(file.name, file.content_type)
    if not filetype or (
        (allowed_attachments != AllowedAttachments.ALL and not filetype.is_media)
        or (allowed_attachments == AllowedAttachments.IMAGES and not filetype.is_image)
    ):
        raise ValidationError(
            message=pgettext(
                "attachment uploaded file validator",
                "%(name)s: uploaded file type is not allowed.",
            ),
            code="attachment_type",
            params={"name": file.name},
        )

    if max_size and file.size > max_size:
        raise ValidationError(
            message=pgettext(
                "attachments file size validator",
                "%(name)s: uploaded file cannot be larger than %(limit_value)s (it has %(show_value)s).",
            ),
            code="attachment_size",
            params={
                "name": file.name,
                "limit_value": str(filesizeformat(max_size)),
                "show_value": str(filesizeformat(file.size)),
            },
        )

    return filetype
