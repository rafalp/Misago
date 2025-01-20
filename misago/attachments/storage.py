from typing import TYPE_CHECKING

from django.db.models import Sum

from .models import Attachment

if TYPE_CHECKING:
    from ..users.models import User

__all__ = [
    "get_total_attachment_storage_usage",
    "get_total_unused_attachments_size",
    "get_user_attachment_storage_usage",
    "get_user_unused_attachments_size",
]


def get_total_attachment_storage_usage() -> int:
    return _get_size_usage(Attachment.objects.all())


def get_total_unused_attachments_size() -> int:
    queryset = Attachment.objects.filter(post__isnull=True)
    return _get_size_usage(queryset)


def get_user_attachment_storage_usage(user: "User") -> int:
    queryset = Attachment.objects.filter(uploader=user)
    return _get_size_usage(queryset)


def get_user_unused_attachments_size(user: "User") -> int:
    queryset = Attachment.objects.filter(uploader=user, post__isnull=True)
    return _get_size_usage(queryset)


def _get_size_usage(queryset) -> int:
    result = queryset.aggregate(uploads=Sum("size"), thumbnails=Sum("thumbnail_size"))

    uploads = result["uploads"] or 0
    thumbnails = result["thumbnails"] or 0
    return uploads + thumbnails
