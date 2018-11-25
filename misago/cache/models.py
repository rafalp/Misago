from django.db import models

from .utils import generate_version_string


class CacheVersion(models.Model):
    cache = models.CharField(max_length=128, primary_key=True)
    version = models.CharField(max_length=8, default=generate_version_string)
