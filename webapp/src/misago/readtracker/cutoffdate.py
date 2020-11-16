from datetime import timedelta

from django.utils import timezone

from ..conf import settings


def get_cutoff_date(settings, user=None):
    cutoff_date = timezone.now() - timedelta(days=settings.readtracker_cutoff)

    if user and user.is_authenticated and user.joined_on > cutoff_date:
        return user.joined_on
    return cutoff_date
