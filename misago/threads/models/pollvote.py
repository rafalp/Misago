from django.conf import settings
from django.db import models
from django.utils import timezone


class PollVote(models.Model):
    category = models.ForeignKey(
        "misago_categories.Category", related_name="+", on_delete=models.CASCADE
    )
    thread = models.ForeignKey(
        "misago_threads.Thread", related_name="+", on_delete=models.CASCADE
    )
    poll = models.ForeignKey(
        "misago_threads.Poll", related_name="+", on_delete=models.CASCADE
    )
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    voter_name = models.CharField(max_length=255)
    voter_slug = models.CharField(max_length=255)
    voted_on = models.DateTimeField(default=timezone.now)
    choice_hash = models.CharField(max_length=12, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["poll", "voter_name"]),
        ]
