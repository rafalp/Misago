from django.conf import settings
from django.db import models
from django.utils import timezone

from ..plugins.models import PluginDataModel


class Like(PluginDataModel):
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    thread = models.ForeignKey("misago_threads.Thread", on_delete=models.CASCADE)
    post = models.ForeignKey("misago_threads.Post", on_delete=models.CASCADE)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    user_name = models.CharField(max_length=255)
    user_slug = models.CharField(max_length=255)

    liked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-id"]
