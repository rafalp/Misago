from django.db import models
from django.utils.translation import ugettext_lazy as _

from misago.core.cache import cache
from misago.core.utils import time_amount


__all__ = [
    'RESTRICT_NO', 'RESTRICT_MODERATOR_REVIEW', 'RESTRICT_DISALLOW',
    'RESTRICTIONS_CHOICES', 'WarningLevel'
]


RESTRICT_NO = 0
RESTRICT_MODERATOR_REVIEW = 1
RESTRICT_DISALLOW = 2


RESTRICTIONS_CHOICES = (
    (RESTRICT_NO, _("No restrictions")),
    (RESTRICT_MODERATOR_REVIEW, _("Review by moderator")),
    (RESTRICT_DISALLOW, _("Disallowed")),
)


class WarningLevel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    level = models.PositiveIntegerField(default=1, db_index=True)
    length_in_minutes = models.PositiveIntegerField(default=0)
    restricts_posting_replies = models.PositiveIntegerField(
        default=RESTRICT_NO)
    restricts_posting_threads = models.PositiveIntegerField(
        default=RESTRICT_NO)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_level()

        super(WarningLevel, self).save(*args, **kwargs)
        cache.delete('warning_levels')

    def delete(self, *args, **kwargs):
        super(WarningLevel, self).delete(*args, **kwargs)
        cache.delete('warning_levels')

    @property
    def length(self):
        if self.length_in_minutes:
            return time_amount(self.length_in_minutes * 60)
        else:
            return _("permanent")

    def set_level(self):
        try:
            self.level = WarningLevel.objects.latest('level').level + 1
        except WarningLevel.DoesNotExist:
            self.level = 1
