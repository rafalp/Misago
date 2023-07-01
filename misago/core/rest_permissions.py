from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous and request.method not in SAFE_METHODS:
            raise PermissionDenied(
                pgettext("api", "This action is not available to guests.")
            )

        return True
