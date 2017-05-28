from django.contrib.postgres.fields import JSONField
from django.db import models

from . import utils


class SettingsGroupsManager(models.Manager):
    def ordered_alphabetically(self):
        from django.utils.translation import ugettext as _

        groups_dict = {}

        for group in self.all():
            groups_dict[_(group.name)] = group

        ordered_groups = []
        for key in groups_dict.keys():
            ordered_groups.append(groups_dict[key])
        return ordered_groups


class SettingsGroup(models.Model):
    key = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    objects = SettingsGroupsManager()


class SettingsManager(models.Manager):
    def change_setting(self, setting, dry_value=None, wet_value=None):
        if dry_value:
            return self.filter(setting=setting).update(dry_value=dry_value)
        elif wet_value:
            try:
                setting = self.get(setting=setting)
                setting.value = wet_value
                setting.save(update_fields=['dry_value'])
            except Setting.DoesNotExist:
                return 0


class Setting(models.Model):
    group = models.ForeignKey(SettingsGroup, on_delete=models.CASCADE)
    setting = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    legend = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0, db_index=True)
    dry_value = models.TextField(null=True, blank=True)
    default_value = models.TextField(null=True, blank=True)
    python_type = models.CharField(max_length=255, default='string')
    is_public = models.BooleanField(default=False)
    is_lazy = models.BooleanField(default=False)
    form_field = models.CharField(max_length=255, default='text')
    field_extra = JSONField()

    objects = SettingsManager()

    @property
    def value(self):
        return utils.get_setting_value(self)

    @value.setter
    def value(self, new_value):
        return utils.set_setting_value(self, new_value)

    @property
    def has_custom_value(self):
        return utils.has_custom_value(self)
