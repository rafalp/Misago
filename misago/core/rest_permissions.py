from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous and request.method not in SAFE_METHODS:
            raise PermissionDenied(_("This action is not available to guests."))
        else:
            return True
