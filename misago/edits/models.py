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

    old_content = models.TextField(null=True, blank=True)
    new_content = models.TextField(null=True, blank=True)
    added_content = models.PositiveIntegerField(default=0)
    removed_content = models.PositiveIntegerField(default=0)

    attachments = models.JSONField(default=list)
    added_attachments = models.PositiveIntegerField(default=0)
    removed_attachments = models.PositiveIntegerField(default=0)

    hidden_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    hidden_by_name = models.CharField(max_length=255, null=True, blank=True)
    hidden_by_slug = models.CharField(max_length=255, null=True, blank=True)

    is_hidden = models.BooleanField(default=False)

    edited_at = models.DateTimeField(default=timezone.now)
    hidden_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]
