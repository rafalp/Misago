from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from misago.users.bans import get_request_ip_ban


def deny_authenticated(f):
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated():
            raise PermissionDenied(
                _("This action is not available to signed in users."))
        else:
            return f(request, *args, **kwargs)
    return decorator


def deny_guests(f):
    def decorator(request, *args, **kwargs):
        if request.user.is_anonymous():
            raise PermissionDenied(
                _("This action is not available to guests."))
        else:
            return f(request, *args, **kwargs)
    return decorator


def deny_banned_ips(f):
    def decorator(request, *args, **kwargs):
        ban = get_request_ip_ban(request)
        if ban:
            raise PermissionDenied(
                _("Your IP address is banned from performing this action."),
                {'ban': ban.get_serialized_message()})
        else:
            return f(request, *args, **kwargs)
    return decorator


def deflect_authenticated(f):
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('misago:index')
        else:
            return f(request, *args, **kwargs)
    return decorator


def deflect_guests(f):
    def decorator(request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect('misago:index')
        else:
            return f(request, *args, **kwargs)
    return decorator


def deflect_banned_ips(f):
    def decorator(request, *args, **kwargs):
        ban = get_request_ip_ban(request)
        if ban:
            return redirect('misago:index')
        else:
            return f(request, *args, **kwargs)
    return decorator
