from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import npgettext, pgettext_lazy

from ...acl import algebra
from ...acl.decorators import return_boolean
from ...acl.models import Role

__all__ = [
    "allow_delete_user",
    "can_delete_user",
    "allow_delete_own_account",
    "can_delete_own_account",
]


class PermissionsForm(forms.Form):
    legend = pgettext_lazy("users delete permission", "Deleting users")

    can_delete_users_newer_than = forms.IntegerField(
        label=pgettext_lazy(
            "users delete permission", "Maximum age of deleted account (in days)"
        ),
        help_text=pgettext_lazy(
            "users delete permission", "Enter zero to disable this check."
        ),
        min_value=0,
        initial=0,
    )
    can_delete_users_with_less_posts_than = forms.IntegerField(
        label=pgettext_lazy(
            "users delete permission", "Maximum number of posts on deleted account"
        ),
        help_text=pgettext_lazy(
            "users delete permission", "Enter zero to disable this check."
        ),
        min_value=0,
        initial=0,
    )


def change_permissions_form(role):
    if isinstance(role, Role) and role.special_role != "anonymous":
        return PermissionsForm


def build_acl(acl, roles, key_name):
    new_acl = {
        "can_delete_users_newer_than": 0,
        "can_delete_users_with_less_posts_than": 0,
    }
    new_acl.update(acl)

    return algebra.sum_acls(
        new_acl,
        roles=roles,
        key=key_name,
        can_delete_users_newer_than=algebra.greater,
        can_delete_users_with_less_posts_than=algebra.greater,
    )


def add_acl_to_user(user_acl, target):
    target.acl["can_delete"] = can_delete_user(user_acl, target)
    if target.acl["can_delete"]:
        target.acl["can_moderate"] = True


def register_with(registry):
    registry.acl_annotator(get_user_model(), add_acl_to_user)


def allow_delete_user(user_acl, target):
    newer_than = user_acl["can_delete_users_newer_than"]
    less_posts_than = user_acl["can_delete_users_with_less_posts_than"]
    if not newer_than and not less_posts_than:
        raise PermissionDenied(
            pgettext_lazy("users delete permission", "You can't delete users.")
        )

    if user_acl["user_id"] == target.id:
        raise PermissionDenied(
            pgettext_lazy("users delete permission", "You can't delete your account.")
        )
    if target.is_misago_admin:
        raise PermissionDenied(
            pgettext_lazy("users delete permission", "Administrators can't be deleted.")
        )
    if target.is_staff:
        raise PermissionDenied(
            pgettext_lazy(
                "users delete permission", "Django staff users can't be deleted."
            )
        )

    if newer_than:
        if target.joined_on < timezone.now() - timedelta(days=newer_than):
            message = npgettext(
                "users delete permission",
                "You can't delete users that are members for more than %(days)s day.",
                "You can't delete users that are members for more than %(days)s days.",
                newer_than,
            )
            raise PermissionDenied(message % {"days": newer_than})
    if less_posts_than:
        if target.posts > less_posts_than:
            message = npgettext(
                "users delete permission",
                "You can't delete users that made more than %(posts)s post.",
                "You can't delete users that made more than %(posts)s posts.",
                less_posts_than,
            )
            raise PermissionDenied(message % {"posts": less_posts_than})


can_delete_user = return_boolean(allow_delete_user)


def allow_delete_own_account(settings, user, target):
    if user.id != target.id:
        raise PermissionDenied(
            pgettext_lazy(
                "users delete permission", "You can't delete other users accounts."
            )
        )

    if not settings.allow_delete_own_account and not user.is_deleting_account:
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


can_delete_own_account = return_boolean(allow_delete_own_account)
