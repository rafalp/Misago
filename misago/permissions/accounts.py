from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext_lazy


def check_delete_own_account_permission(user):
    if user.is_misago_admin:
        raise PermissionDenied(
            pgettext_lazy(
                "users delete permission",
                "You can't delete your account because you are an administrator.",
            )
        )

    if user.is_staff:
        raise PermissionDenied(
            pgettext_lazy(
                "users delete permission",
                "You can't delete your account because you are a staff user.",
            )
        )
