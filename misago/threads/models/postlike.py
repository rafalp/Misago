from django.conf import settings
from django.db import models
from django.utils import timezone


class PostLike(models.Model):
    category = models.ForeignKey(
        "misago_categories.Category",
        related_name="+",
        on_delete=models.CASCADE,
    )
    thread = models.ForeignKey(
        "misago_threads.Thread",
        related_name="+",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        "misago_threads.Post",
        related_name="+",
        on_delete=models.CASCADE,
    )

    liker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    liker_name = models.CharField(max_length=255, db_index=True)
    liker_slug = models.CharField(max_length=255)

    liked_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-id"]
