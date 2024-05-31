from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext_lazy


def allow_delete_own_account(user):
    if user.is_deleting_account:
        raise PermissionDenied(
            pgettext_lazy("users delete permission", "You can't delete your account.")
        )

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
