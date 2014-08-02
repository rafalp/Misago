from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from misago.acl import algebra
from misago.acl.decorators import require_target_type, return_boolean
from misago.acl.models import Role
from misago.core import forms


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("Users moderation")

    can_rename_users = forms.YesNoSwitch(label=_("Can rename users"))
    can_ban_users = forms.YesNoSwitch(label=_("Can ban users"))
    max_ban_length = forms.IntegerField(
        label=_("Max length, in days, of imposed ban"),
        help_text=_("Enter zero to let moderators impose permanent bans."),
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
        'can_rename_users': 0,
        'can_ban_users': 0,
        'max_ban_length': 2,
    }
    new_acl.update(acl)

    return algebra.sum_acls(
            new_acl, roles=roles, key=key_name,
            can_rename_users=algebra.greater,
            can_ban_users=algebra.greater,
            max_ban_length=algebra.greater_or_zero
            )


"""
ACL's for targets
"""
@require_target_type(get_user_model())
def add_acl_to_target(user, acl, target):
    target.acl_['can_rename'] = can_rename_user(user, target)
    target.acl_['can_ban'] = can_ban_user(user, target)
    target.acl_['max_ban_length'] = user.acl['max_ban_length']

    for permission in ('can_rename', 'can_ban'):
        if target.acl_[permission]:
            target.acl_['can_moderate'] = True
            break


"""
ACL tests
"""
def allow_rename_user(user, target):
    if not user.acl['can_rename_users']:
        raise PermissionDenied(_("You can't rename users."))
    if not user.is_superuser and (target.is_staff or target.is_superuser):
        raise PermissionDenied(_("You can't rename administrators."))
can_rename_user = return_boolean(allow_rename_user)


def allow_ban_user(user, target):
    if not user.acl['can_ban_users']:
        raise PermissionDenied(_("You can't ban users."))
    if target.is_staff or target.is_superuser:
        raise PermissionDenied(_("You can't ban administrators."))
can_ban_user = return_boolean(allow_ban_user)
