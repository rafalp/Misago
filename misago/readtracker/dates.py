from datetime import timedelta

from django.conf import settings
from django.utils import timezone


def is_date_tracked(user, date):
    if date:
        return date > user.joined_on
    else:
        return False
