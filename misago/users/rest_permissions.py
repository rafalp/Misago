from rest_framework.permissions import BasePermission, AllowAny, SAFE_METHODS

from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.users.bans import get_request_ip_ban


__all__ = [
    'AllowAny',
    'IsAuthenticatedOrReadOnly',
    'UnbannedOnly',
    'UnbannedAnonOnly'
]


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous() and request.method not in SAFE_METHODS:
            raise PermissionDenied(
                _("This action is not available to guests."))
        else:
            return True


class UnbannedOnly(BasePermission):
    def is_request_banned(self, request):
        ban = get_request_ip_ban(request)
        if ban:
            raise PermissionDenied(
                _("Your IP address is banned from performing this action."),
                {'ban': ban.get_serialized_message()})

    def has_permission(self, request, view):
        self.is_request_banned(request)
        return True


class UnbannedAnonOnly(UnbannedOnly):
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            raise PermissionDenied(
                _("This action is not available to signed in users."))

        self.is_request_banned(request)
        return True
