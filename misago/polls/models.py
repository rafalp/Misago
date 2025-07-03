from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from ..plugins.models import PluginDataModel


class Poll(PluginDataModel):
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    thread = models.OneToOneField("misago_threads.Thread", on_delete=models.CASCADE)

    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )
    starter_name = models.CharField(max_length=255)
    starter_slug = models.CharField(max_length=255)

    started_at = models.DateTimeField(default=timezone.now)
    closed_at = models.DateTimeField(blank=True, null=True)

    question = models.CharField(max_length=255)
    choices = models.JSONField()
    duration = models.PositiveIntegerField(default=0)

    max_choices = models.PositiveIntegerField(default=1)
    can_change_vote = models.BooleanField(default=False)

    is_public = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    votes = models.PositiveIntegerField(default=0)

    closed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    closed_by_name = models.CharField(max_length=255, null=True, blank=True)
    closed_by_slug = models.CharField(max_length=255, null=True, blank=True)

    @property
    def ends_at(self) -> datetime | None:
        if not self.duration:
            return None

        return self.started_at + timedelta(days=self.duration)

    @property
    def has_ended(self) -> bool:
        if self.duration:
            return timezone.now() >= self.ends_at

        return False


class PollVote(models.Model):
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    thread = models.ForeignKey("misago_threads.Thread", on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_id = models.CharField(max_length=12, db_index=True)

    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )
    voter_name = models.CharField(max_length=255)
    voter_slug = models.CharField(max_length=255)

    voted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["poll", "choice_id"]),
            models.Index(fields=["poll", "voter_name"]),
        ]
