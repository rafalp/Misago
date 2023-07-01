from typing import TYPE_CHECKING

from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext

if TYPE_CHECKING:
    from misago.users.models import User


def allow_use_notifications(user: "User"):
    if user.is_anonymous:
        raise PermissionDenied(
            pgettext(
                "notifications permission",
                "You must be signed in to access your notifications.",
            )
        )
