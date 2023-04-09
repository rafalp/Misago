from typing import TYPE_CHECKING

from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _

if TYPE_CHECKING:
    from misago.users.models import User


def allow_use_notifications(user: "User"):
    if user.is_anonymous:
        raise PermissionDenied(_("You must be signed in to access your notifications."))
