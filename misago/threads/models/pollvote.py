from django.conf import settings
from django.db import models
from django.utils import timezone


class PollVote(models.Model):
    category = models.ForeignKey('misago_categories.Category')
    thread = models.ForeignKey('misago_threads.Thread')
    poll = models.ForeignKey('misago_threads.Poll')
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    voter_name = models.CharField(max_length=255)
    voter_slug = models.CharField(max_length=255)
    voter_ip = models.GenericIPAddressField()
    voted_on = models.DateTimeField(default=timezone.now)
    choice_hash = models.CharField(max_length=12, db_index=True)

    class Meta:
        index_together = [
            ['poll', 'voter_name'],
        ]
