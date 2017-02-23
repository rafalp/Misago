from rest_framework.permissions import BasePermission

from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.core.exceptions import Banned
from misago.users.bans import get_request_ip_ban
from misago.users.models import Ban


class UnbannedOnly(BasePermission):
    def is_request_banned(self, request):
        ban = get_request_ip_ban(request)
        if ban:
            hydrated_ban = Ban(
                check_type=Ban.IP,
                user_message=ban['message'],
                expires_on=ban['expires_on'],
            )
            raise Banned(hydrated_ban)

    def has_permission(self, request, view):
        self.is_request_banned(request)
        return True


class UnbannedAnonOnly(UnbannedOnly):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            raise PermissionDenied(_("This action is not available to signed in users."))

        self.is_request_banned(request)
        return True
