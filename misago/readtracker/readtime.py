from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional

from django.utils import timezone

from ..conf.dynamicsettings import DynamicSettings

if TYPE_CHECKING:
    from ..users.models import User


def get_default_read_time(
    settings: DynamicSettings,
    user: Optional["User"] = None,
) -> datetime:
    min_read_time = timezone.now() - timedelta(days=settings.readtracker_cutoff)

    if user and user.is_authenticated and user.joined_on > min_read_time:
        return user.joined_on

    return min_read_time
