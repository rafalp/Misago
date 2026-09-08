from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from ..categories.models import Category
from ..threads.models import Post, Thread


class ThreadSearch(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thread = models.OneToOneField(Thread, on_delete=models.CASCADE, primary_key=True)
    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
    )

    title = models.TextField()
    search_vector = SearchVectorField()

    started_at = models.DateTimeField(db_index=True)

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
    )

    content = models.TextField()
    thread_search_vector = SearchVectorField()
    post_search_vector = SearchVectorField()

    posted_at = models.DateTimeField(db_index=True)

    is_first_post = models.BooleanField(default=False)

    class Meta:
        indexes = [
            GinIndex(fields=["post_search_vector"]),
            GinIndex(fields=["thread_search_vector"]),
            models.Index(
                fields=["thread_id"],
                condition=models.Q(is_first_post=True),
                name="search_post_search_is_firs_idx",
            ),
        ]
