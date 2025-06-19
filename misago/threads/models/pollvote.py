from django.conf import settings
from django.db import models
from django.utils import timezone


class PollVote(models.Model):
    category = models.ForeignKey(
        "misago_categories.Category", on_delete=models.CASCADE, related_name="+"
    )
    thread = models.ForeignKey(
        "misago_threads.Thread", on_delete=models.CASCADE, related_name="+"
    )
    poll = models.ForeignKey(
        "misago_threads.Poll", on_delete=models.CASCADE, related_name="+"
    )
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    voter_name = models.CharField(max_length=255)
    voter_slug = models.CharField(max_length=255)
    voted_on = models.DateTimeField(default=timezone.now)
    choice_hash = models.CharField(max_length=12, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["poll", "voter_name"]),
        ]
