from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from rest_framework.permissions import SAFE_METHODS, AllowAny, BasePermission

from misago.core.exceptions import Banned
from misago.users.bans import get_request_ip_ban
from misago.users.models import BAN_IP, Ban


__all__ = [
    'AllowAny',
    'IsAuthenticatedOrReadOnly',
    'UnbannedOnly',
    'UnbannedAnonOnly'
]


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous() and request.method not in SAFE_METHODS:
            raise PermissionDenied(_("This action is not available to guests."))
        else:
            return True


class UnbannedOnly(BasePermission):
    def is_request_banned(self, request):
        ban = get_request_ip_ban(request)
        if ban:
            hydrated_ban = Ban(
                check_type=BAN_IP,
                user_message=ban['message'],
                expires_on=ban['expires_on'])
            raise Banned(hydrated_ban)

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
