from django.conf import settings
from django.db import models
from django.utils import timezone


class PostRead(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    thread = models.ForeignKey("misago_threads.Thread", on_delete=models.CASCADE)
    post = models.ForeignKey("misago_threads.Post", on_delete=models.CASCADE)
    last_read_on = models.DateTimeField(default=timezone.now)
