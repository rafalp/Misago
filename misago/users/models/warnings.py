from collections import OrderedDict
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from misago.core import threadstore
from misago.core.cache import cache
from misago.core.utils import time_amount


__all__ = [
    'RESTRICT_NO', 'RESTRICT_MODERATOR_REVIEW', 'RESTRICT_DISALLOW',
    'RESTRICTIONS_CHOICES', 'WarningLevel', 'UserWarning'
]


CACHE_NAME = 'misago_warning_levels'

RESTRICT_NO = 0
RESTRICT_MODERATOR_REVIEW = 1
RESTRICT_DISALLOW = 2


RESTRICTIONS_CHOICES = (
    (RESTRICT_NO, _("No restrictions")),
    (RESTRICT_MODERATOR_REVIEW, _("Review by moderator")),
    (RESTRICT_DISALLOW, _("Disallowed")),
)


class WarningLevelManager(models.Manager):
    def dict(self):
        return self.get_levels_from_threadstore()

    def get_levels_from_threadstore(self):
        levels = threadstore.get(CACHE_NAME, 'nada')
        if levels == 'nada':
            levels = self.get_levels_from_cache()
            threadstore.set(CACHE_NAME, levels)
        return levels

    def get_levels_from_cache(self):
        levels = cache.get(CACHE_NAME, 'nada')
        if levels == 'nada':
            levels = self.get_levels_from_database()
            cache.set(CACHE_NAME, levels)
        return levels

    def get_levels_from_database(self):
        levels = [(0, None)]
        for level, obj in enumerate(self.order_by('level')):
            levels.append((level + 1, obj))
        return OrderedDict(levels)


class WarningLevel(models.Model):
    name = models.CharField(max_length=255)
    level = models.PositiveIntegerField(default=1, db_index=True)
    length_in_minutes = models.PositiveIntegerField(default=0)
    restricts_posting_replies = models.PositiveIntegerField(
        default=RESTRICT_NO)
    restricts_posting_threads = models.PositiveIntegerField(
        default=RESTRICT_NO)

    objects = WarningLevelManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_level()

        super(WarningLevel, self).save(*args, **kwargs)
        cache.delete(CACHE_NAME)

    def delete(self, *args, **kwargs):
        super(WarningLevel, self).delete(*args, **kwargs)
        cache.delete(CACHE_NAME)

    @property
    def length(self):
        if self.length_in_minutes:
            return time_amount(self.length_in_minutes * 60)
        else:
            return _("permanent")

    @property
    def has_restrictions(self):
        return self.restricts_posting_replies or self.restricts_posting_threads

    @property
    def is_replying_moderated(self):
        return self.restricts_posting_replies == RESTRICT_MODERATOR_REVIEW

    @property
    def is_replying_disallowed(self):
        return self.restricts_posting_replies == RESTRICT_DISALLOW

    @property
    def is_starting_threads_moderated(self):
        return self.restricts_posting_threads == RESTRICT_MODERATOR_REVIEW

    @property
    def is_starting_threads_disallowed(self):
        return self.restricts_posting_threads == RESTRICT_DISALLOW

    def set_level(self):
        try:
            self.level = WarningLevel.objects.latest('level').level + 1
        except WarningLevel.DoesNotExist:
            self.level = 1


class UserWarning(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="warnings")
    reason = models.TextField(null=True, blank=True)
    given_on = models.DateTimeField(default=timezone.now)
    giver = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, blank=True,
                              on_delete=models.SET_NULL,
                              related_name="warnings_given")
    giver_username = models.CharField(max_length=255)
    giver_slug = models.CharField(max_length=255)
    is_canceled = models.BooleanField(default=False)
    canceled_on = models.DateTimeField(null=True, blank=True)
    canceler = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name="warnings_canceled")
    canceler_username = models.CharField(max_length=255)
    canceler_slug = models.CharField(max_length=255)

    def cancel(self, canceler):
        self.is_canceled = True
        self.canceled_on = timezone.now()
        self.canceler = canceler
        self.canceler_username = canceler.username
        self.canceler_slug = canceler.slug

        self.save(update_fields=(
            'is_canceled',
            'canceled_on',
            'canceler',
            'canceler_username',
            'canceler_slug',
        ))

    def is_expired(self, valid_for):
        return timezone.now() > self.given_on + timedelta(minutes=valid_for)
