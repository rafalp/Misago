from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext

from ..threads.models import ThreadParticipant
from .hooks import check_private_threads_permission_hook
from .proxy import UserPermissionsProxy


def check_private_threads_permission(permissions: UserPermissionsProxy):
    return check_private_threads_permission_hook(
        _check_private_threads_permission_action, permissions
    )


def _check_private_threads_permission_action(permissions: UserPermissionsProxy):
    if permissions.user.is_anonymous:
        raise PermissionDenied(
            pgettext(
                "private threads permission error",
                "You must be signed in to use private threads.",
            )
        )

    if not permissions.can_use_private_threads:
        raise PermissionDenied(
            pgettext(
                "private threads permission error",
                "You can't use private threads.",
            )
        )


def filter_private_threads_queryset(user_permissions: UserPermissionsProxy, queryset):
    if user_permissions.user.is_anonymous:
        return queryset.none()

    return queryset.filter(
        id__in=ThreadParticipant.objects.filter(user=user_permissions.user).values(
            "thread_id"
        )
    )
