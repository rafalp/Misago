import os
from functools import cached_property
from hashlib import md5

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string

from ..conf import settings
from ..core.utils import slugify
from ..plugins.models import PluginDataModel
from .filetypes import AttachmentFileType, filetypes


def upload_to(instance, filename):
    # pylint: disable=undefined-loop-variable
    spread_path = md5(str(instance.secret[:16]).encode()).hexdigest()
    secret = Attachment.get_new_secret()

    filename_lowered = filename.lower().strip()
    for extension in instance.filetype.extensions:
        if filename_lowered.endswith(extension):
            break

    filename_clean = ".".join(
        (slugify(filename[: (len(extension) + 1) * -1])[:16], extension)
    )

    return os.path.join(
        "attachments", spread_path[:2], spread_path[2:4], secret[:32], filename_clean
    )


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

    secret = models.CharField(max_length=64)

    filename = models.CharField(max_length=255, db_index=True)
    size = models.PositiveIntegerField(default=0, db_index=True)

    filetype_name = models.CharField(max_length=100, null=True)
    dimensions = models.CharField(max_length=15, null=True)

    thumbnail = models.ImageField(
        max_length=255,
        blank=True,
        null=True,
        upload_to=upload_to,
    )
    image = models.ImageField(
        max_length=255,
        blank=True,
        null=True,
        upload_to=upload_to,
    )
    video = models.FileField(
        max_length=255,
        blank=True,
        null=True,
        upload_to=upload_to,
    )
    file = models.FileField(
        max_length=255,
        blank=True,
        null=True,
        upload_to=upload_to,
    )

    is_deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.filename

    def delete(self, *args, **kwargs):
        self.delete_files()
        return super().delete(*args, **kwargs)

    def delete_files(self):
        if self.thumbnail:
            self.thumbnail.delete(save=False)
        if self.image:
            self.image.delete(save=False)
        if self.video:
            self.video.delete(save=False)
        if self.file:
            self.file.delete(save=False)

    @classmethod
    def get_new_secret(cls):
        return get_random_string(64)

    @cached_property
    def filetype(self) -> AttachmentFileType | None:
        try:
            return filetypes.get_filetype(self.filetype_name)
        except ValueError:
            return None

    @property
    def is_image(self):
        return bool(self.image)

    @property
    def is_video(self):
        return bool(self.video)

    @property
    def is_file(self):
        return bool(self.file)

    @property
    def url(self) -> str:
        return (self.image or self.video or self.file).url

    @property
    def thumbnail_url(self) -> str | None:
        return self.thumbnail.url if self.thumbnail else None

    def get_absolute_url(self):
        return reverse(
            "misago:attachment", kwargs={"pk": self.pk, "secret": self.secret}
        )

    def get_thumbnail_url(self):
        if self.thumbnail:
            return reverse(
                "misago:attachment-thumbnail",
                kwargs={"pk": self.pk, "secret": self.secret},
            )
