from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from ..plugins.models import PluginDataModel


class ThreadEventQuerySet(models.QuerySet):
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


class ThreadEvent(PluginDataModel):
    category = models.ForeignKey(
        "misago_categories.Category",
        on_delete=models.DO_NOTHING,
    )
    thread = models.ForeignKey(
        "misago_threads.Thread",
        on_delete=models.DO_NOTHING,
        related_name="events",
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    actor_name = models.CharField(max_length=255, blank=True, null=True)
    actor_slug = models.CharField(max_length=255, blank=True, null=True)

    hidden_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hidden_by_name = models.CharField(max_length=255, blank=True, null=True)
    hidden_by_slug = models.CharField(max_length=255, blank=True, null=True)

    event_type = models.CharField(max_length=32)

    detail = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey(ContentType,blank=True,null=True, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")
    items = models.PositiveIntegerField(blank=True, null=True)

    is_hidden = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    hidden_at = models.DateTimeField(blank=True, null=True)

    objects = ThreadEventQuerySet.as_manager()

    class Meta(PluginDataModel.Meta):
        indexes = PluginDataModel.Meta.indexes + [
            models.Index(
                name="misago_thread_event_created",
                fields=["thread", "created_at"],
            ),
            models.Index(
                name="misago_thread_event_content",
                fields=["content_type", "object_id"],
                condition=models.Q(object_id__isnull=False),
            ),
        ]

    @property
    def content_model(self) -> type[models.Model] | None:
        if not self.content_type:
            return None

        try:
            app_label, model_name = self.content_type.split(".")
            return apps.get_model(app_label, model_name)
        except LookupError:
            return None

    def get_content_id(self, content_type: str) -> int | None:
        if self.content_type == content_type:
            return self.object_id

        return None

    def clear_context_object(self):
        self.content_type = None
        self.object_id = None
