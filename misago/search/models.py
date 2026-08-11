from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models


class PostSearch(models.Model):
    post_id = models.PositiveIntegerField(primary_key=True)

    category_id = models.PositiveIntegerField(db_index=True)
    thread_id = models.PositiveIntegerField(db_index=True)
    poster_id = models.PositiveIntegerField(db_index=True)

    thread_title = SearchVectorField(null=True)
    post_content = SearchVectorField()

    posted_at = models.DateTimeField(db_index=True)

    is_thread_pinned = models.BooleanField(default=False)
    incoming_links = models.PositiveIntegerField(default=0)
    is_hidden = models.BooleanField()
    is_unapproved = models.BooleanField()

    class Meta:
        indexes = [
            GinIndex(fields=["thread_title"]),
            GinIndex(fields=["post_content"]),
        ]
