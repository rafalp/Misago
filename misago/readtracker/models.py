from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class ForumRead(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    forum = models.ForeignKey('misago_forums.Forum')
    last_read_on = models.DateTimeField()


class ThreadRead(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    forum = models.ForeignKey('misago_forums.Forum')
    thread = models.ForeignKey('misago_threads.Thread')
    read_replies =  models.PositiveIntegerField(default=0)
    last_read_on = models.DateTimeField()
