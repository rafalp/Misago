from django.core.exceptions import PermissionDenied
from django.template.defaultfilters import date as format_date
from django.utils.translation import gettext_lazy as _

from misago.users.bans import is_ip_banned


def deny_authenticated(f):
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated():
            raise PermissionDenied(
                _("This page is not available to signed in users."))
        else:
            return f(request, *args, **kwargs)
    return decorator


def deny_guests(f):
    def decorator(request, *args, **kwargs):
        if request.user.is_anonymous():
            raise PermissionDenied(
                _("This page is not available to guests."))
        else:
            return f(request, *args, **kwargs)
    return decorator


def deny_banned_ips(f):
    def decorator(request, *args, **kwargs):
        ban = is_ip_banned(request)
        if ban:
            default_message = _("Your IP address has been banned.")
            ban_message = ban.get('message') or default_message
            if ban.get('valid_until'):
                ban_expires = format_date(ban['valid_until'])
                expiration_message = _("This ban will expire on %(date)s.")
                expiration_message = expiration_message % {'date': ban_expires}
                ban_message = '%s\n\n%s' % (ban_message, expiration_message)
            raise PermissionDenied(ban_message)
        else:
            return f(request, *args, **kwargs)
    return decorator

