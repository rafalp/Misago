from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone


class Poll(models.Model):
    category = models.ForeignKey('misago_categories.Category')
    thread = models.OneToOneField('misago_threads.Thread')
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    poster_name = models.CharField(max_length=255)
    poster_slug = models.CharField(max_length=255)
    poster_ip = models.GenericIPAddressField()

    posted_on = models.DateTimeField(default=timezone.now)
    length = models.PositiveIntegerField(default=0)

    question = models.CharField(max_length=255)
    choices = JSONField()
    allowed_choices = models.PositiveIntegerField(default=1)
    allow_revotes = models.BooleanField(default=False)

    votes = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=False)
