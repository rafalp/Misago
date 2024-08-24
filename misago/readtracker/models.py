from django.conf import settings
from django.db import models
from django.utils import timezone


class ReadCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    read_time = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["user", "category"]),
        ]


class ReadThread(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    thread = models.ForeignKey("misago_threads.Thread", on_delete=models.CASCADE)
    read_time = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["user", "thread"]),
        ]
