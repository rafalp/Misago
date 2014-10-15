from datetime import timedelta

from django.conf import settings
from django.utils import timezone


def is_date_tracked(user, date):
    if date:
        return date > user.reads_cutoff
    else:
        return False
