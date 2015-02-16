from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

from misago.users.bans import get_request_ip_ban


def deny_authenticated(f):
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.is_ajax():
                message = _("This action is not available to signed in users.")
            else:
                message = _("This page is not available to signed in users.")
            raise PermissionDenied(message)
        else:
            return f(request, *args, **kwargs)
    return decorator


def deny_guests(f):
    def decorator(request, *args, **kwargs):
        if request.user.is_anonymous():
            if request.is_ajax():
                message = _("This action is not available to guests.")
            else:
                message = _("This page is not available to guests.")
            raise PermissionDenied(message)
        else:
            return f(request, *args, **kwargs)
    return decorator


def deny_banned_ips(f):
    def decorator(request, *args, **kwargs):
        ban = get_request_ip_ban(request)
        if ban:
            default_message = _("Your IP address has been banned.")
            ban_message = ban.get('message') or default_message

            if ban.get('expires'):
                ban_expires = ban['formatted_expiration_date']
                expiration_message = _("This ban will end on %(date)s.")
                expiration_message = expiration_message % {'date': ban_expires}
                ban_message = '%s\n\n%s' % (ban_message, expiration_message)
            raise PermissionDenied(ban_message)
        else:
            return f(request, *args, **kwargs)
    return decorator
