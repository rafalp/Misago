from django.utils.timezone import make_aware, utc

from .conf import OLD_FORUM
from .db import fetch_assoc


def localise_datetime(datetime):
    if datetime:
        return make_aware(datetime, utc)
    return None
