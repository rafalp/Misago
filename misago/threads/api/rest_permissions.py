from rest_framework.permissions import BasePermission

from ..permissions.privatethreads import allow_use_private_threads


class PrivateThreadsPermission(BasePermission):
    def has_permission(self, request, view):
        allow_use_private_threads(request.user)

        return True
