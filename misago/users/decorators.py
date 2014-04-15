from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _


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
