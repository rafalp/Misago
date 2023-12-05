from typing import Any

from django.contrib.postgres.indexes import GinIndex
from django.db import models


class PluginDataModel(models.Model):
    plugin_data = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        abstract = True
        indexes = [GinIndex(fields=["plugin_data"])]

    def plugin_data_in(self, key: str) -> bool:
        if self.plugin_data is None:
            return False

        return key in self.plugin_data

    def plugin_data_get(self, key: str, default=None) -> Any:
        if self.plugin_data is None:
            return default

        return self.plugin_data.get(key, default)

    def plugin_data_set(self, key: str, value: Any):
        if self.plugin_data is None:
            self.plugin_data = {}

        self.plugin_data[key] = value

    def plugin_data_update(self, value: dict):
        if self.plugin_data is None:
            self.plugin_data = {}

        self.plugin_data.update(value)
