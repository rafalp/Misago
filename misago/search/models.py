from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models


class ThreadSearch(models.Model):
    category_id = models.PositiveIntegerField(db_index=True)
    thread_id = models.PositiveIntegerField(primary_key=True)
    starter_id = models.PositiveIntegerField(null=True)

    title = models.TextField()
    search_vector = SearchVectorField()

    started_at = models.DateTimeField(db_index=True)

    is_pinned = models.BooleanField(default=False)

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),
            models.Index(
                fields=["starter_id"],
                condition=models.Q(starter_id__isnull=False),
                name="search_thread_search_start_idx",
            ),
        ]


class PostSearch(models.Model):
    category_id = models.PositiveIntegerField(db_index=True)
    thread_id = models.PositiveIntegerField(db_index=True)
    post_id = models.PositiveIntegerField(primary_key=True)
    poster_id = models.PositiveIntegerField(null=True)

    content = models.TextField()
    thread_search_vector = SearchVectorField()
    post_search_vector = SearchVectorField()

    posted_at = models.DateTimeField(db_index=True)

    is_thread_pinned = models.BooleanField(default=False)
    incoming_links = models.PositiveIntegerField(default=0)

    is_first_post = models.BooleanField(default=False)
    is_hidden = models.BooleanField()
    is_unapproved = models.BooleanField()

    class Meta:
        indexes = [
            GinIndex(fields=["post_search_vector"]),
            GinIndex(fields=["thread_search_vector"]),
            models.Index(
                fields=["thread_id"],
                condition=models.Q(is_first_post=True),
                name="search_post_search_is_firs_idx",
            ),
            models.Index(
                fields=["poster_id"],
                condition=models.Q(poster_id__isnull=False),
                name="search_post_search_poster_idx",
            ),
        ]
