from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ungettext

from misago.acl import algebra
from misago.acl.decorators import require_target_type, return_boolean
from misago.acl.models import Role
from misago.core import forms


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("Deleting users")

    can_delete_users_newer_than = forms.IntegerField(
        label=_("Maximum age of deleted account (in days)"),
        help_text=_("Enter zero to disable this check."),
        min_value=0,
        initial=0)
    can_delete_users_with_less_posts_than = forms.IntegerField(
        label=_("Maximum number of posts on deleted account"),
        help_text=_("Enter zero to disable this check."),
        min_value=0,
        initial=0)


def change_permissions_form(role):
    if isinstance(role, Role) and role.special_role != 'anonymous':
        return PermissionsForm
    else:
        return None


"""
ACL Builder
"""
def build_acl(acl, roles, key_name):
    new_acl = {
        'can_delete_users_newer_than': 0,
        'can_delete_users_with_less_posts_than': 0,
    }
    new_acl.update(acl)

    return algebra.sum_acls(
            new_acl, roles=roles, key=key_name,
            can_delete_users_newer_than=algebra.greater,
            can_delete_users_with_less_posts_than=algebra.greater
            )


"""
ACL's for targets
"""
@require_target_type(get_user_model())
def add_acl_to_target(user, acl, target):
    target.acl_['can_delete'] = can_delete_user(user, target)
    if target.acl_['can_delete']:
        target.acl_['can_moderate'] = True


"""
ACL tests
"""
def allow_delete_user(user, target):
    newer_than = user.acl['can_delete_users_newer_than']
    less_posts_than = user.acl['can_delete_users_with_less_posts_than']
    if not (newer_than or less_posts_than):
        raise PermissionDenied(_("You can't delete users."))

    if user.pk == target.pk:
        raise PermissionDenied(_("You can't delete yourself."))
    if target.is_staff or target.is_superuser:
        raise PermissionDenied(_("You can't delete administrators."))

    if newer_than:
        if target.joined_on < timezone.now() - timedelta(days=newer_than):
            message = ungettext("You can't delete users that are "
                                "members for more than %(days)s day.",
                                "You can't delete users that are "
                                "members for more than %(days)s days.",
                                newer_than) % {'days': newer_than}
            raise PermissionDenied(message)
    if less_posts_than:
        if target.posts > less_posts_than:
            message = ungettext(
                "You can't delete users that made more than %(posts)s post.",
                "You can't delete users that made more than %(posts)s posts.",
                less_posts_than) % {'posts': less_posts_than}
            raise PermissionDenied(message)
can_delete_user = return_boolean(allow_delete_user)
