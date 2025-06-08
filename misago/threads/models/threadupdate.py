from django.conf import settings
from django.db import models

from ...plugins.models import PluginDataModel
from .thread import Thread


class ThreadUpdate(PluginDataModel):
    category = models.ForeignKey(
        "misago_categories.Category",
        on_delete=models.DO_NOTHING,
    )
    thread = models.ForeignKey(
        Thread,
        on_delete=models.DO_NOTHING,
        related_name="updates",
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    actor_name = models.CharField(max_length=255, blank=True, null=True)

    action = models.CharField(max_length=32)

    context_type = models.CharField(max_length=255, blank=True, null=True)
    context_id = models.CharField(max_length=255, blank=True, null=True)
    context_name = models.CharField(max_length=255, blank=True, null=True)

    is_hidden = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            *PluginDataModel.Meta.indexes,
            models.Index(
                name="misago_thread_update_created",
                fields=["thread", "created_at"],
            ),
            models.Index(
                name="misago_thread_update_context",
                fields=["context_type", "context_id"],
                condition=models.Q(context_id__isnull=False),
            ),
        ]
