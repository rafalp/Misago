import os
from functools import cached_property
from hashlib import sha256
from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string

from ..conf import settings
from ..plugins.models import PluginDataModel
from .filetypes import AttachmentFileType, filetypes

if TYPE_CHECKING:
    from ..threads.models import Post


def upload_to(instance: "Attachment", filename: str) -> str:
    salt = sha256(get_random_string(32).encode()).hexdigest()
    filename, extension = instance.filetype.split_name(filename.lower())
    filename_clean = filename[:16] + "." + extension

    return os.path.join("attachments", salt[:2], salt[2:4], salt[-32:], filename_clean)


class Attachment(PluginDataModel):
    category = models.ForeignKey(
        "misago_categories.Category",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    thread = models.ForeignKey(
        "misago_threads.Thread",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    post = models.ForeignKey(
        "misago_threads.Post",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    uploader_name = models.CharField(max_length=255)
    uploader_slug = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(default=timezone.now, db_index=True)

    name = models.CharField(max_length=255, db_index=True)
    slug = models.CharField(max_length=255)

    filetype_id = models.CharField(max_length=10, null=True)

    upload = models.FileField(max_length=255, upload_to=upload_to)
    dimensions = models.CharField(max_length=15, null=True)
    size = models.PositiveIntegerField(default=0)

    thumbnail = models.FileField(max_length=255, upload_to=upload_to)
    thumbnail_dimensions = models.CharField(max_length=15, null=True)
    thumbnail_size = models.PositiveIntegerField(default=0)

    is_deleted = models.BooleanField(default=False, db_index=True)

    upload_key: str  # or missing

    class Meta:
        indexes = [
            *PluginDataModel.Meta.indexes,
            models.Index(
                name="misago_attachment_miss_upload",
                fields=["upload"],
                condition=models.Q(upload=""),
            ),
        ]

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.delete_files()
        return super().delete(*args, **kwargs)

    def delete_files(self):
        if self.upload:
            self.upload.delete(save=False)
        if self.thumbnail:
            self.thumbnail.delete(save=False)

    def associate_with_post(self, post: "Post"):
        self.category = post.category
        self.thread = post.thread
        self.post = post

    @cached_property
    def filetype(self) -> AttachmentFileType | None:
        if not self.filetype_id:
            raise ValueError(f"Attachment '{self.name}' is missing 'filetype_id'")

        try:
            return filetypes.get_filetype(self.filetype_id)
        except ValueError:
            return None

    @property
    def filetype_name(self) -> str:
        return str(self.filetype.name)

    @property
    def content_type(self) -> str:
        return self.filetype.content_types[0]

    @property
    def width(self) -> int | None:
        if self.dimensions:
            return int(self.dimensions.split("x")[0])

        return None

    @property
    def height(self) -> int | None:
        if self.dimensions:
            return int(self.dimensions.split("x")[1])

        return None

    @property
    def ratio(self) -> str | None:
        if self.dimensions:
            return (
                ("{:0.2f}".format(self.height * 100 / self.width))
                .rstrip("0")
                .rstrip(".")
            )

        return None

    @property
    def thumbnail_width(self) -> int | None:
        if self.thumbnail_dimensions:
            return int(self.thumbnail_dimensions.split("x")[0])

        return None

    @property
    def thumbnail_height(self) -> int | None:
        if self.thumbnail_dimensions:
            return int(self.thumbnail_dimensions.split("x")[1])

        return None

    def get_absolute_url(self) -> str:
        return reverse(
            "misago:attachment-download", kwargs={"id": self.id, "slug": self.slug}
        )

    def get_thumbnail_url(self) -> str | None:
        if not self.thumbnail:
            return None

        return reverse(
            "misago:attachment-thumbnail",
            kwargs={"id": self.id, "slug": self.slug},
        )

    def get_delete_url(self) -> str:
        return reverse(
            "misago:attachment-delete",
            kwargs={"id": self.id, "slug": self.slug},
        )

    def get_details_url(self) -> str:
        return reverse(
            "misago:attachment-details",
            kwargs={"id": self.id, "slug": self.slug},
        )
