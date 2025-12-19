from django.conf import settings
from django.db import models
from django.utils import timezone

from ..plugins.models import PluginDataModel


class PostEdit(PluginDataModel):
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

    edit_reason = models.CharField(max_length=255, null=True, blank=True)

    original_old = models.TextField()
    original_new = models.TextField()
    original_added = models.PositiveIntegerField(default=0)
    original_removed = models.PositiveIntegerField(default=0)

    attachments = models.JSONField(default=list)
    attachments_added = models.PositiveIntegerField(default=0)
    attachments_removed = models.PositiveIntegerField(default=0)

    edited_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-id"]
