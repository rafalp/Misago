from rest_framework.permissions import BasePermission, AllowAny, SAFE_METHODS

from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.users.bans import get_request_ip_ban


__all__ = [
    'AllowAny',
    'IsAuthenticatedOrReadOnly',
    'UnbannedAnonOnly'
]


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous() and request.method not in SAFE_METHODS:
            raise PermissionDenied(
                _("This action is not available to guests."))
        else:
            return True


class UnbannedAnonOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            raise PermissionDenied(
                _("This action is not available to signed in users."))

        ban = get_request_ip_ban(request)
        if ban:
            raise PermissionDenied(
                _("Your IP address is banned from performing this action."),
                {'ban': ban.get_serialized_message()})

        return True
