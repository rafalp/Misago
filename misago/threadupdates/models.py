from django.apps import apps
from django.conf import settings
from django.db import models

from ..plugins.models import PluginDataModel


class ThreadUpdateQuerySet(models.QuerySet):
    def context_object(self, obj: models.Model):
        return self.filter(
            context_type=f"{obj._meta.app_label}.{obj._meta.model_name}",
            context_id=obj.pk,
        )

    def context_type(self, obj: models.Model | type[models.Model]):
        context_type = f"{obj._meta.app_label}.{obj._meta.model_name}"
        return self.filter(context_type=context_type)

    def clear_context_objects(self) -> int:
        return self.update(context_type=None, context_id=None)


class ThreadUpdate(PluginDataModel):
    category = models.ForeignKey(
        "misago_categories.Category",
        on_delete=models.DO_NOTHING,
    )
    thread = models.ForeignKey(
        "misago_threads.Thread",
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

    hidden_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hidden_by_name = models.CharField(max_length=255, blank=True, null=True)

    action = models.CharField(max_length=32)

    context = models.CharField(max_length=255, blank=True, null=True)
    context_type = models.CharField(max_length=255, blank=True, null=True)
    context_id = models.PositiveIntegerField(blank=True, null=True)

    is_hidden = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    hidden_at = models.DateTimeField(blank=True, null=True)

    objects = ThreadUpdateQuerySet.as_manager()

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

    @property
    def context_model(self) -> type[models.Model] | None:
        if not self.context_type:
            return None

        try:
            app_label, model_name = self.context_type.split(".")
            return apps.get_model(app_label, model_name)
        except LookupError:
            return None

    def get_context_id(self, context_type: str) -> int | None:
        if self.context_type == context_type:
            return self.context_id

        return None

    def clear_context_object(self):
        self.context_type = None
        self.context_id = None
