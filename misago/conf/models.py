from django.contrib.postgres.fields import JSONField
from django.db import models

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
    dry_value = models.TextField(null=True, blank=True)
    python_type = models.CharField(max_length=255, default="string")
    is_public = models.BooleanField(default=False)
    is_lazy = models.BooleanField(default=False)

    objects = SettingsManager()

    @property
    def value(self):
        return hydrate_value(self.python_type, self.dry_value)

    @value.setter
    def value(self, new_value):
        if new_value is not None:
            self.dry_value = dehydrate_value(self.python_type, new_value)
        else:
            self.dry_value = None
        return new_value
