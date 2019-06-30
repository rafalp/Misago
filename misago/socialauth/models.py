from django.contrib.postgres.fields import JSONField
from django.db import models

from .providers import providers


class SocialAuthProvider(models.Model):
    provider = models.CharField(primary_key=True, max_length=30)
    button_text = models.CharField(max_length=255, null=True, blank=True)
    button_color = models.CharField(max_length=7, null=True, blank=True)
    settings = JSONField(default=dict)
    is_active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return providers.get_name(self.provider)
