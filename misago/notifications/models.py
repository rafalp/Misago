import cgi

from django.conf import settings
from django.db import models
from django.utils import timezone


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='notifications')
    is_new = models.BooleanField(default=True)
    date = models.DateTimeField(default=timezone.now, db_index=True)
    trigger = models.CharField(max_length=8)
    message = models.TextField()
    url = models.TextField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                           on_delete=models.SET_NULL,
                           related_name='notifications_by',
                           blank=True, null=True)
    sender_username = models.CharField(max_length=255, blank=True, null=True)
    sender_slug = models.CharField(max_length=255, blank=True, null=True)
