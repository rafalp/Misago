from django.conf import settings
from django.db import models
from django.utils import timezone


def clean_upload_to(instance, filename):
    instance.filename = filename



class Attachment(models.Model):
    uuid = models.CharField(max_length=64, db_index=True)
    type = models.ForeignKey('AttachmentType')
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
    file = models.FileField(upload_to=clean_upload_to)

    downloads = models.PositiveIntegerField(default=0)
