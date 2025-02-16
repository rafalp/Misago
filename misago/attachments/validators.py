from logging import getLogger
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.template.defaultfilters import filesizeformat
from django.utils.translation import npgettext, pgettext

from ..permissions.proxy import UserPermissionsProxy
from .enums import (
    AllowedAttachments,
    AttachmentStorage,
    AttachmentTypeRestriction,
)
from .filetypes import AttachmentFileType, filetypes
from .storage import (
    get_total_unused_attachments_size,
    get_user_attachment_storage_usage,
    get_user_unused_attachments_size,
)

if TYPE_CHECKING:
    from ..users.models import User

logger = getLogger("misago.attachments.validators")


def validate_post_attachments_limit(value: int, limit_value: int):
    if value > limit_value:
        raise ValidationError(
            message=npgettext(
                "post attachments limit validator",
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
    allowed_attachments: AllowedAttachments | str,
    max_size: int = 0,
    storage: AttachmentStorage | None = None,
    storage_limit: int = 0,
    storage_left: int = 0,
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
                "%(name)s: uploaded file cannot exceed %(limit_value)s in size (it has %(show_value)s).",
            ),
            code="attachment_size",
            params={
                "name": file.name,
                "limit_value": str(filesizeformat(max_size)),
                "show_value": str(filesizeformat(file.size)),
            },
        )

    if storage_limit and storage_left < file.size:
        if storage == AttachmentStorage.GLOBAL:
            logger.error("Global unused attachments storage limit exceeded")

            raise ValidationError(
                message=pgettext(
                    "attachments file storage left validator",
                    "%(name)s: uploaded file exceeds the remaining attachments space (%(limit_value)s).",
                ),
                code="attachments_global_storage_left",
                params={
                    "name": file.name,
                    "limit_value": str(filesizeformat(storage_left)),
                },
            )

        raise ValidationError(
            message=pgettext(
                "attachments file storage left validator",
                "%(name)s: uploaded file exceeds your remaining attachment space (%(limit_value)s).",
            ),
            code="attachments_storage_left",
            params={
                "name": file.name,
                "limit_value": str(filesizeformat(storage_left)),
            },
        )

    return filetype


def get_attachments_storage_constraints(
    global_unused_limit: int,
    permissions: UserPermissionsProxy,
) -> dict:
    user = permissions.user

    # Global limit comes from setting that holds value in MB
    global_unused_limit = global_unused_limit * 1024 * 1024
    user_storage_limit = permissions.attachment_storage_limit
    user_unused_limit = permissions.unused_attachments_storage_limit

    if not any((global_unused_limit, user_storage_limit, user_unused_limit)):
        return {"storage": None, "storage_limit": 0, "storage_left": 0}

    limits: list[int] = []

    if global_unused_limit:
        limits.append(
            (
                AttachmentStorage.GLOBAL,
                global_unused_limit,
                global_unused_limit - get_total_unused_attachments_size(),
            )
        )

    if user_storage_limit:
        limits.append(
            (
                AttachmentStorage.USER_TOTAL,
                user_storage_limit,
                user_storage_limit - get_user_attachment_storage_usage(user),
            )
        )

    if user_unused_limit:
        limits.append(
            (
                AttachmentStorage.USER_UNUSED,
                user_unused_limit,
                user_unused_limit - get_user_unused_attachments_size(user),
            )
        )

    storage, storage_limit, storage_left = min(limits, key=lambda k: k[2])
    return {
        "storage": storage,
        "storage_limit": storage_limit,
        "storage_left": max(storage_left, 0),
    }


def validate_uploaded_file_extension(
    file: UploadedFile,
    restriction: AttachmentTypeRestriction,
    extensions: list[str],
):
    if not extensions:
        return

    if restriction == AttachmentTypeRestriction.REQUIRE:
        validate_uploaded_file_required_extension(file, extensions)
    elif restriction == AttachmentTypeRestriction.DISALLOW:
        validate_uploaded_file_disallowed_extension(file, extensions)


def validate_uploaded_file_required_extension(
    file: UploadedFile, extensions: list[str]
):
    if not extensions:
        return

    filename = file.name.lower()
    for extension in extensions:
        if filename.endswith("." + extension):
            return
    _raise_extension_not_allowed(file)


def validate_uploaded_file_disallowed_extension(
    file: UploadedFile, extensions: list[str]
):
    if not extensions:
        return

    filename = file.name.lower()
    for extension in extensions:
        if filename.endswith("." + extension):
            _raise_extension_not_allowed(file)


def _raise_extension_not_allowed(file: UploadedFile):
    raise ValidationError(
        message=pgettext(
            "attachment uploaded file validator",
            "%(name)s: uploaded file type is not allowed.",
        ),
        code="attachment_extension",
        params={"name": file.name},
    )
