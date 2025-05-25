from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils import timezone


class PostSnapshot(models.Model):
    post_id = models.PositiveIntegerField(db_index=True)

    original = models.TextField()
    parsed = models.TextField()
    checksum = models.CharField(max_length=64)

    search_document = models.TextField(null=True, blank=True)
    search_vector = SearchVectorField()

    created_at = models.DateTimeField(default=timezone.now)
