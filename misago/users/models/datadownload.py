from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def get_data_upload_to(instance, filename):
    raise NotImplementedError() # todo: generate secure upload to path


class DataDownload(models.Model):
    STATUS_PENDING = 0
    STATUS_PROCESSING = 1
    STATUS_READY = 2
    STATUS_EXPIRED = 3

    STATUS_CHOICES = (
        (STATUS_PENDING, _("Pending")),
        (STATUS_PROCESSING, _("Processing")),
        (STATUS_READY, _("Ready")),
        (STATUS_EXPIRED, _("Expired")),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    status = models.PositiveIntegerField(
        default=STATUS_PENDING,
        choices=STATUS_CHOICES,
        db_index=True,
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    requester_name = models.CharField(max_length=255)
    requested_on = models.DateTimeField(default=timezone.now)
    expires_on = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to=get_data_upload_to, null=True, blank=True)

    class Meta:
        ordering = ['-pk']
