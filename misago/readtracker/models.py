from django.conf import settings
from django.db import models


class CategoryRead(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        'misago_categories.Category',
        on_delete=models.CASCADE,
    )
    last_read_on = models.DateTimeField()


class ThreadRead(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        'misago_categories.Category',
        on_delete=models.CASCADE,
    )
    thread = models.ForeignKey(
        'misago_threads.Thread',
        on_delete=models.CASCADE,
    )
    last_read_on = models.DateTimeField()
