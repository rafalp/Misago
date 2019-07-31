from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class DeletedUser(models.Model):
    DELETED_BY_USER = 1
    DELETED_BY_STAFF = 2
    DELETED_BY_SYSTEM = 3

    DELETED_BY_CHOICES = (
        (DELETED_BY_USER, _('By user')),
        (DELETED_BY_STAFF, _('By staff')),
        (DELETED_BY_SYSTEM, _('By system')),
    )

    deleted_on = models.DateTimeField(default=timezone.now)
    deleted_by = models.CharField(
        max_length=50,
        choices=DELETED_BY_CHOICES,
        db_index=True
    )

    class Meta:
        ordering = ['-deleted_on']
