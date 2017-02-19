from django.conf import settings
from django.db import models


class CategoryRead(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey('misago_categories.Category')
    last_read_on = models.DateTimeField()


class ThreadRead(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey('misago_categories.Category')
    thread = models.ForeignKey('misago_threads.Thread')
    last_read_on = models.DateTimeField()
