from datetime import datetime, timedelta

from django.utils import timezone

from ..core.utils import slugify
from ..users.models import User


FactoryTimestampArg = datetime | timedelta | int | None
FactoryUserArg = User | str | None


def factory_timestamp_arg(
    timestamp: FactoryTimestampArg,
) -> tuple[User, str, str | None]:
    if timestamp is True:
        return timezone.now()

    if isinstance(timestamp, datetime):
        return timestamp

    if isinstance(timestamp, timedelta):
        return timezone.now() - timestamp

    if isinstance(timestamp, int):
        if timestamp != 0:
            return timezone.now() + timedelta(seconds=timestamp)
        return timezone.now()

    return None


def unpack_factory_user_arg(user: FactoryUserArg) -> tuple[User, str, str | None]:
    if isinstance(user, str):
        return None, user, slugify(user)

    if isinstance(user, User):
        return user, user.username, user.slug

    return None, None, None
