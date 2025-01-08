import os
from functools import cached_property
from hashlib import md5
from io import BytesIO

from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
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
    secret = Attachment.generate_new_secret()

    filename_lowered = filename.lower().strip()
    for extension in instance.filetype.extensions:
        if filename_lowered.endswith(extension):
            break

    filename_clean = ".".join(
        (slugify(filename[: (len(extension) + 1) * -1])[:16], extension)
    )

    return os.path.join(
        "attachments", spread_path[:2], spread_path[2:4], secret, filename_clean
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
    def generate_new_secret(cls):
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
    def url(self):
        return (self.image or self.video or self.file).url

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

    def set_image(self, upload: UploadedFile):
        fileformat = self.filetype.extensions[0]

        self.image = File(upload, upload.name)

        thumbnail = Image.open(upload)
        downscale_image = (
            thumbnail.size[0] > settings.MISAGO_ATTACHMENT_IMAGE_SIZE_LIMIT[0]
            or thumbnail.size[1] > settings.MISAGO_ATTACHMENT_IMAGE_SIZE_LIMIT[1]
        )
        strip_animation = fileformat == "gif"

        thumb_stream = BytesIO()
        if downscale_image:
            thumbnail.thumbnail(settings.MISAGO_ATTACHMENT_IMAGE_SIZE_LIMIT)
            if fileformat == "jepg":
                thumbnail.save(thumb_stream, "jpeg")
            else:
                thumbnail.save(thumb_stream, "png")
        elif strip_animation:
            thumbnail.save(thumb_stream, "png")

        if downscale_image or strip_animation:
            self.thumbnail = ContentFile(thumb_stream.getvalue(), upload.name)

    def set_video(self, upload: UploadedFile):
        self.video = File(upload, upload.name)

    def set_file(self, upload: UploadedFile):
        self.file = File(upload, upload.name)
