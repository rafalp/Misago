from datetime import timedelta

from django.conf import settings
from django.utils import timezone


def cutoff_date():
    return timezone.now() - timedelta(days=settings.MISAGO_READ_RECORD_LENGTH)


def is_date_tracked(date):
    if date:
        return date > cutoff_date()
    else:
        return False
