from django.db import models
from django.utils import timezone

from misago.conf import settings


class Report(models.Model):
    category = models.ForeignKey('misago_categories.Category')
    thread = models.ForeignKey('misago_threads.Thread')
    post = models.ForeignKey('misago_threads.Post')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    null=True, blank=True,
                                    on_delete=models.SET_NULL)
    reported_by_name = models.CharField(max_length=255)
    reported_by_slug = models.CharField(max_length=255)
    reported_by_ip = models.GenericIPAddressField()
    reported_on = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    checksum = models.CharField(max_length=64, default='-')

    is_closed = models.BooleanField(default=False)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  null=True, blank=True, db_index=True,
                                  on_delete=models.SET_NULL,
                                  related_name='closedreport_set')
    closed_by_name = models.CharField(max_length=255)
    closed_by_slug = models.CharField(max_length=255)
    closed_on = models.DateTimeField(default=timezone.now)
