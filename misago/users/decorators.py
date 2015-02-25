from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from misago.users.bans import get_request_ip_ban


def deny_authenticated(f):
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.is_ajax():
                raise PermissionDenied(
                    _("This action is not available to signed in users."))
            else:
                return redirect('misago:index')
        else:
            return f(request, *args, **kwargs)
    return decorator


def deny_guests(f):
    def decorator(request, *args, **kwargs):
        if request.user.is_anonymous():
            if request.is_ajax():
                raise PermissionDenied(
                    _("This action is not available to guests."))
            else:
                return redirect('misago:index')
        else:
            return f(request, *args, **kwargs)
    return decorator


def deny_banned_ips(f):
    def decorator(request, *args, **kwargs):
        ban = get_request_ip_ban(request)
        if ban:
            if request.is_ajax():
                raise PermissionDenied(ban.get_serialized_message())
            else:
                return redirect('misago:index')
        else:
            return f(request, *args, **kwargs)
    return decorator
