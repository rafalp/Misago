from django.conf import settings
from django.db import models
from django.utils import timezone


class PrivateThreadMember(models.Model):
    thread = models.ForeignKey("misago_threads.Thread", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_owner = models.BooleanField(default=False)
