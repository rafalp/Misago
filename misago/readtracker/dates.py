from datetime import timedelta

from django.conf import settings
from django.utils import timezone


def is_date_tracked(date, user, category_read_cutoff=None):
    if date:
        cutoff_date = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)

        if cutoff_date < user.joined_on:
            cutoff_date = user.joined_on
        if category_read_cutoff and cutoff_date < category_read_cutoff:
            cutoff_date = category_read_cutoff

        return date > cutoff_date
    else:
        return False
