import os
from hashlib import md5
from io import BytesIO

from PIL import Image

from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.encoding import python_2_unicode_compatible

from misago.conf import settings
from misago.core.utils import slugify


def upload_to(instance, filename):
    spread_path = md5(str(instance.secret[:16]).encode()).hexdigest()
    secret = Attachment.generate_new_secret()

    filename_lowered = filename.lower().strip()
    for extension in instance.filetype.extensions_list:
        if filename_lowered.endswith(extension):
            break

    filename_clean = '.'.join((slugify(filename[:(len(extension) + 1) * -1])[:16], extension))

    return os.path.join('attachments', spread_path[:2], spread_path[2:4], secret, filename_clean)


@python_2_unicode_compatible
class Attachment(models.Model):
    secret = models.CharField(max_length=64)
    filetype = models.ForeignKey('AttachmentType')
    post = models.ForeignKey('Post', blank=True, null=True, on_delete=models.SET_NULL)

    uploaded_on = models.DateTimeField(default=timezone.now, db_index=True)

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )
    uploader_name = models.CharField(max_length=255)
    uploader_slug = models.CharField(max_length=255, db_index=True)
    uploader_ip = models.GenericIPAddressField()

    filename = models.CharField(max_length=255, db_index=True)
    size = models.PositiveIntegerField(default=0, db_index=True)

    thumbnail = models.ImageField(max_length=255, blank=True, null=True, upload_to=upload_to)
    image = models.ImageField(max_length=255, blank=True, null=True, upload_to=upload_to)
    file = models.FileField(max_length=255, blank=True, null=True, upload_to=upload_to)

    def __str__(self):
        return self.filename

    def delete(self, *args, **kwargs):
        self.delete_files()
        return super(Attachment, self).delete(*args, **kwargs)

    def delete_files(self):
        if self.thumbnail:
            self.thumbnail.delete(save=False)
        if self.image:
            self.image.delete(save=False)
        if self.file:
            self.file.delete(save=False)

    @classmethod
    def generate_new_secret(cls):
        return get_random_string(settings.MISAGO_ATTACHMENT_SECRET_LENGTH)

    @property
    def is_image(self):
        return bool(self.image)

    @property
    def is_file(self):
        return not self.is_image

    def get_absolute_url(self):
        return reverse(
            'misago:attachment', kwargs={
                'pk': self.pk,
                'secret': self.secret,
            }
        )

    def get_thumbnail_url(self):
        if self.thumbnail:
            return reverse(
                'misago:attachment-thumbnail', kwargs={
                    'pk': self.pk,
                    'secret': self.secret,
                }
            )
        else:
            return None

    def set_file(self, upload):
        self.file = File(upload, upload.name)

    def set_image(self, upload):
        fileformat = self.filetype.extensions_list[0]

        self.image = File(upload, upload.name)

        thumbnail = Image.open(upload)
        downscale_image = (
            thumbnail.size[0] > settings.MISAGO_ATTACHMENT_IMAGE_SIZE_LIMIT[0]
            or thumbnail.size[1] > settings.MISAGO_ATTACHMENT_IMAGE_SIZE_LIMIT[1]
        )
        strip_animation = fileformat == 'gif'

        thumb_stream = BytesIO()
        if downscale_image:
            thumbnail.thumbnail(settings.MISAGO_ATTACHMENT_IMAGE_SIZE_LIMIT)
            if fileformat == 'jpg':
                # normalize jpg to jpeg for Pillow
                thumbnail.save(thumb_stream, 'jpeg')
            else:
                thumbnail.save(thumb_stream, fileformat)
        elif strip_animation:
            thumbnail.save(thumb_stream, fileformat)

        if downscale_image or strip_animation:
            self.thumbnail = ContentFile(thumb_stream.getvalue(), upload.name)
