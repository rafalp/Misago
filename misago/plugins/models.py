from typing import Any

from django.contrib.postgres.indexes import GinIndex
from django.db import models


class PluginDataModel(models.Model):
    plugin_data = models.JSONField(default=dict)

    class Meta:
        abstract = True
        indexes = [GinIndex(fields=["plugin_data"])]
