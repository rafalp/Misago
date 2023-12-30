from django.utils.translation import pgettext

from ..admin.views.generic import PermissionsFormView
from .enums import CategoryPermission


def get_admin_category_permissions(form: PermissionsFormView) -> list[dict]:
    perms = (
        form.create_permission(
            id=CategoryPermission.SEE,
            name=pgettext("category permission", "See category"),
            help_text=pgettext(
                "category permission", "See category on categories lists."
            ),
            color="#eff6ff",
        ),
        form.create_permission(
            id=CategoryPermission.READ,
            name=pgettext("category permission", "Read threads"),
            color="#f5f3ff",
        ),
        form.create_permission(
            id=CategoryPermission.START,
            name=pgettext("category permission", "Start threads"),
            color="#fef2f2",
        ),
        form.create_permission(
            id=CategoryPermission.REPLY,
            name=pgettext("category permission", "Reply threads"),
            color="#fefce8",
        ),
        form.create_permission(
            id=CategoryPermission.ATTACHMENTS,
            name=pgettext("category permission", "Attachments"),
            help_text=pgettext(
                "category permission", "Upload and download attachments."
            ),
            color="#ecfdf5",
        ),
    )

    return perms
