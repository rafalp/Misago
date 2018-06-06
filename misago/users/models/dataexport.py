from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def get_export_upload_to(instance, filename):
    raise NotImplementedError() # todo: generate secure upload to path


class DataExport(models.Model):
    STATUS_REQUESTED = 0
    STATUS_PROCESSING = 1
    STATUS_READY = 2
    STATUS_EXPIRED = 3

    STATUS_CHOICES = (
        (STATUS_REQUESTED, _("Requested")),
        (STATUS_PROCESSING, _("Processing")),
        (STATUS_READY, _("Ready")),
        (STATUS_EXPIRED, _("Expired")),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    status = models.PositiveIntegerField(
        default=STATUS_REQUESTED,
        choices=STATUS_CHOICES,
        db_index=True,
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    requested_on = models.DateTimeField(default=timezone.now)
    expires_on = models.DateTimeField(default=timezone.now)
    export_file = models.FileField(upload_to=get_export_upload_to, null=True, blank=True)
