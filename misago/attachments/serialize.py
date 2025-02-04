from django.template.defaultfilters import filesizeformat

from .filetypes import AttachmentFileType
from .hooks import serialize_attachment_hook
from .models import Attachment


def serialize_attachment(attachment: Attachment) -> dict:
    return serialize_attachment_hook(_serialize_attachment_action, attachment)


def _serialize_attachment_action(attachment: Attachment) -> dict:
    return {
        "id": attachment.id,
        "key": getattr(attachment, "upload_key", None),
        "name": attachment.name,
        "url": attachment.get_details_url(),
        "uploader": _serialize_uploader(attachment),
        "filetype": _serialize_filetype(attachment.filetype),
        "content_type": attachment.content_type,
        "dimensions": _serialize_dimensions(attachment.dimensions),
        "upload": _serialize_file(attachment.upload, attachment.size),
        "thumbnail": _serialize_file(attachment.thumbnail, attachment.thumbnail_size),
    }


def _serialize_uploader(attachment: Attachment) -> dict:
    if attachment.uploader:
        return {
            "id": attachment.uploader.id,
            "username": attachment.uploader.username,
        }

    return {
        "id": None,
        "username": attachment.uploader_name,
    }


def _serialize_filetype(filetype: AttachmentFileType) -> dict:
    return {
        "id": filetype.id,
        "name": str(filetype.name),
        "is_media": filetype.is_media,
        "is_video": filetype.is_video,
    }


def _serialize_dimensions(dimensions: str | None) -> list[int] | None:
    if not dimensions:
        return None

    return [int(v) for v in dimensions.split("x")]


def _serialize_file(file, size: int) -> dict:
    if not file:
        return None

    return {
        "url": file.url,
        "size": {"bytes": size, "formatted": str(filesizeformat(size))},
    }
