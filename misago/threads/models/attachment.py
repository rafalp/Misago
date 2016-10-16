from io import BytesIO

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from PIL import Image


class Attachment(models.Model):
    uuid = models.CharField(max_length=64)
    filetype = models.ForeignKey('AttachmentType')
    post = models.ForeignKey(
        'Post',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    uploaded_on = models.DateTimeField(default=timezone.now)

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    uploader_name = models.CharField(max_length=255)
    uploader_slug = models.CharField(max_length=255)
    uploader_ip = models.GenericIPAddressField()

    filename = models.CharField(max_length=255)

    thumbnail = models.ImageField(blank=True, null=True, upload_to='attachments')
    image = models.ImageField(blank=True, null=True, upload_to='attachments')
    file = models.FileField(blank=True, null=True, upload_to='attachments')

    downloads = models.PositiveIntegerField(default=0)

    @classmethod
    def generate_new_uuid(cls):
        return get_random_string(settings.MISAGO_ATTACHMENT_SECRET_LENGTH)

    @property
    def is_image(self):
        return bool(self.image)

    @property
    def is_file(self):
        return not self.is_image

    def get_absolute_url(self):
        return reverse('misago:attachment', kwargs={
            'pk': self.pk,
            'uuid': self.uuid,
        })

    def get_thumbnail_url(self):
        if self.is_image:
            return reverse('misago:attachment-thumbnail', kwargs={
                'pk': self.pk,
                'uuid': self.uuid,
            })
        else:
            return None

    def set_file(self, upload):
        file_secret = get_random_string(settings.MISAGO_ATTACHMENT_SECRET_LENGTH)
        self.file = File(upload, '.'.join([file_secret, self.filetype.extensions_list[0]]))

    def set_image(self, upload):
        fileformat = self.filetype.extensions_list[0]

        image_secret = get_random_string(settings.MISAGO_ATTACHMENT_SECRET_LENGTH)
        image_filename = '.'.join([image_secret, fileformat])
        self.image = File(upload, image_filename)

        thumbnail = Image.open(upload)
        thumbnail.thumbnail((500, 500))

        thumb_stream = BytesIO()
        thumbnail.save(thumb_stream, fileformat)

        thumb_secret = get_random_string(settings.MISAGO_ATTACHMENT_SECRET_LENGTH)
        thumb_filename = '.'.join([thumb_secret, fileformat])
        self.thumbnail = ContentFile(thumb_stream.get_value(), thumb_filename)
