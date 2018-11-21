from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


DELETED_BY_USER = 1
DELETED_BY_STAFF = 2
DELETED_BY_SYSTEM = 3

DELETED_BY_CHOICES = (
    (DELETED_BY_USER, _('By User')),
    (DELETED_BY_STAFF, _('By Staff')),
    (DELETED_BY_SYSTEM, _('By System')),
)


class DeletedUser(models.Model):
    deleted_on = models.DateTimeField(default=timezone.now)
    deleted_by = models.PositiveIntegerField(
        choices=DELETED_BY_CHOICES,
        default=1
    )

    class Meta:
        ordering = ['deleted_on']
        db_index = True
