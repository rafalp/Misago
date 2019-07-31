from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


DELETED_BY_USER = 'by_user'
DELETED_BY_STAFF = 'by_staff'
DELETED_BY_SYSTEM = 'by_system'

DELETED_BY_CHOICES = (
    (DELETED_BY_USER, _('By User')),
    (DELETED_BY_STAFF, _('By Staff')),
    (DELETED_BY_SYSTEM, _('By System')),
)


class DeletedUser(models.Model):
    deleted_on = models.DateTimeField(default=timezone.now)
    deleted_by = models.CharField(
        max_length=50,
        choices=DELETED_BY_CHOICES,
        default=DELETED_BY_USER
    )

    class Meta:
        ordering = ['deleted_on']
        db_index = True
