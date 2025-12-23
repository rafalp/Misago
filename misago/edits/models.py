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

    old_title = models.CharField(max_length=255, null=True, blank=True)
    new_title = models.CharField(max_length=255, null=True, blank=True)

    old_content = models.TextField()
    new_content = models.TextField()
    added_content = models.PositiveIntegerField(default=0)
    removed_content = models.PositiveIntegerField(default=0)

    attachments = models.JSONField(default=list)
    added_attachments = models.PositiveIntegerField(default=0)
    removed_attachments = models.PositiveIntegerField(default=0)

    edited_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-id"]
