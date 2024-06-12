from functools import wraps

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.translation import pgettext

from ..core.exceptions import Banned
from .bans import get_request_ip_ban
from .models import Ban


def deny_authenticated(f):
    @wraps(f)
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated:
            raise PermissionDenied(
                pgettext(
                    "block authenticated decorator",
                    "This page is not available to signed in users.",
                )
            )
        else:
            return f(request, *args, **kwargs)

    return decorator


def deny_banned_ips(f):
    @wraps(f)
    def decorator(request, *args, **kwargs):
        ban = get_request_ip_ban(request)
        if ban:
            hydrated_ban = Ban(
                check_type=Ban.IP,
                user_message=ban["message"],
                expires_on=ban["expires_on"],
            )
            raise Banned(hydrated_ban)
        else:
            return f(request, *args, **kwargs)

    return decorator
