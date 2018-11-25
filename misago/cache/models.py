from django.db import models

from .utils import get_random_version


class CacheVersion(models.Model):
    cache = models.CharField(max_length=128, primary_key=True)
    version = models.CharField(max_length=8, default=get_random_version)
