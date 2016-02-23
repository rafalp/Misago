from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class CategoryRead(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey('misago_categories.Category')
    last_read_on = models.DateTimeField()


class ThreadRead(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey('misago_categories.Category')
    thread = models.ForeignKey('misago_threads.Thread')
    read_replies =  models.PositiveIntegerField(default=0)
    last_read_on = models.DateTimeField()
