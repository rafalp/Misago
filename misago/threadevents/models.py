from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from ..plugins.models import PluginDataModel


class ThreadEventQuerySet(models.QuerySet):
    def content_object(self, obj: models.Model):
        return self.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
        )

    def content_type(self, obj: models.Model | type[models.Model]):
        return self.filter(content_type=ContentType.objects.get_for_model(obj))

    def clear_content_objects(self) -> int:
        return self.update(content_type=None, object_id=None)


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
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
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

        return ContentType.objects.get_for_id(self.content_type_id).model_class()

    def get_object_id_for_type(self, obj_type: models.Model) -> int | None:
        if self.content_type and self.content_type == ContentType.objects.get_for_model(
            obj_type
        ):
            return self.object_id

        return None
