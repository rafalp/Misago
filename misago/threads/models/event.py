from django.db import models
from django.utils import timezone

from misago.conf import settings

from misago.threads.checksums import is_event_valid


class Event(models.Model):
    forum = models.ForeignKey('misago_forums.Forum')
    thread = models.ForeignKey('Thread')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                               on_delete=models.SET_NULL)
    author_name = models.CharField(max_length=255)
    author_slug = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    occured_on = models.DateTimeField(default=timezone.now, db_index=True)
    message = models.CharField(max_length=255)
    checksum = models.CharField(max_length=64, default='-')
    is_hidden = models.BooleanField(default=False)

    @property
    def is_valid(self):
        return is_event_valid(self)

    def set_author(self, user):
        self.author = user
        self.author_name = user.username
        self.author_slug = user.slug
