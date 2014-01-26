from django.db import models


class VersionControl(models.Model):
    key = models.CharField(max_length=128)
    version = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'misago_core'
