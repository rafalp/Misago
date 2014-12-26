from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from misago.notifications.checksums import is_valid


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='misago_notifications')
    is_new = models.BooleanField(default=True)
    date = models.DateTimeField(default=timezone.now)
    hash = models.CharField(max_length=8)
    message = models.TextField()
    checksum = models.CharField(max_length=64, default='-')
    url = models.TextField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               related_name='misago_notifications_by',
                               blank=True, null=True)
    sender_username = models.CharField(max_length=255, blank=True, null=True)
    sender_slug = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        index_together = [
            ['user', 'hash'],
        ]

    @property
    def is_valid(self):
        return is_valid(self)

    def get_absolute_url(self):
        if self.is_new:
            return reverse('misago:go_to_notification', kwargs={
                'notification_id': self.id,
                'hash': self.hash
            })
        else:
            return self.url
