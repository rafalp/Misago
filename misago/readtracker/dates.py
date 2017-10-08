from datetime import timedelta

from django.utils import timezone

from misago.conf import settings


def get_cutoff_date(user=None):
    cutoff_date = timezone.now() - timedelta(
        days=settings.MISAGO_READTRACKER_CUTOFF,
    )

    if user and user.is_authenticated and user.joined_on > cutoff_date:
        return user.joined_on
    return cutoff_date


def is_date_tracked(date, user):
    if date:
        cutoff_date = get_cutoff_date()

        if cutoff_date < user.joined_on:
            cutoff_date = user.joined_on

        return date > cutoff_date
    else:
        return False
