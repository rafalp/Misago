from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _


__all__ = [
    'authenticated_only',
    'anonymous_only',
]


def authenticated_only(f):
    def perm_decorator(user, target):
        if user.is_authenticated:
            return f(user, target)
        else:
            messsage = _("You have to sig in to perform this action.")
            raise PermissionDenied(messsage)

    return perm_decorator


def anonymous_only(f):
    def perm_decorator(user, target):
        if user.is_anonymous:
            return f(user, target)
        else:
            messsage = _("Only guests can perform this action.")
            raise PermissionDenied(messsage)

    return perm_decorator
