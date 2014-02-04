from django.db import models


class CacheVersion(models.Model):
    cache = models.CharField(max_length=128)
    version = models.PositiveIntegerField(default=0)
