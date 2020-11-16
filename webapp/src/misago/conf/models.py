from pathlib import Path

from django.contrib.postgres.fields import JSONField
from django.db import models

from ..core.utils import get_file_hash
from .hydrators import dehydrate_value, hydrate_value


class SettingsManager(models.Manager):
    def change_setting(self, setting, dry_value=None, wet_value=None):
        if dry_value:
            return self.filter(setting=setting).update(dry_value=dry_value)

        if wet_value:
            try:
                setting = self.get(setting=setting)
                setting.value = wet_value
                setting.save(update_fields=["dry_value"])
            except Setting.DoesNotExist:
                return 0


class Setting(models.Model):
    setting = models.CharField(max_length=255, unique=True)
    python_type = models.CharField(max_length=255, default="string")
    dry_value = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to="conf",
        height_field="image_height",
        width_field="image_width",
        null=True,
        blank=True,
    )
    image_size = models.PositiveIntegerField(null=True, blank=True)
    image_width = models.PositiveIntegerField(null=True, blank=True)
    image_height = models.PositiveIntegerField(null=True, blank=True)
    is_public = models.BooleanField(default=False)
    is_lazy = models.BooleanField(default=False)

    objects = SettingsManager()

    @property
    def image_dimensions(self):
        if self.image_width and self.image_height:
            return self.image_width, self.image_height
        return None

    @property
    def value(self):
        if self.python_type == "image":
            return self.image
        return hydrate_value(self.python_type, self.dry_value)

    @value.setter
    def value(self, new_value):
        if new_value is not None:
            if self.python_type == "image":
                rename_image_file(new_value, self.setting)
                self.image = new_value
                self.image_size = new_value.size
            else:
                self.dry_value = dehydrate_value(self.python_type, new_value)
        else:
            self.dry_value = None
        return new_value


def rename_image_file(file_obj, prefix):
    name_parts = [
        prefix.replace("_", "-"),
        get_file_hash(file_obj),
        Path(file_obj.name).suffix.strip(".").lower(),
    ]
    file_obj.name = ".".join(name_parts)
