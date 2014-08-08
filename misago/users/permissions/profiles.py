from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from misago.acl import algebra
from misago.acl.decorators import require_target_type, return_boolean
from misago.acl.models import Role
from misago.core import forms

from misago.users.permissions.decorators import authenticated_only


"""
Admin Permissions Form
"""
CAN_SEARCH_USERS = forms.YesNoSwitch(
    label=_("Can search user profiles"),
    initial=1)
CAN_SEE_USER_NAME_HISTORY = forms.YesNoSwitch(
    label=_("Can see other members name history"))
CAN_SEE_BAN_DETAILS = forms.YesNoSwitch(
    label=_("Can see members bans details"),
    help_text=_("Allows users with this permission to see user and "
                "staff ban messages."))


class LimitedPermissionsForm(forms.Form):
    legend = _("User profiles")
    can_search_users = CAN_SEARCH_USERS
    can_see_users_name_history = CAN_SEE_USER_NAME_HISTORY
    can_see_ban_details = CAN_SEE_BAN_DETAILS


class PermissionsForm(LimitedPermissionsForm):
    can_search_users = CAN_SEARCH_USERS
    can_follow_users = forms.YesNoSwitch(
        label=_("Can follow other users"),
        initial=1)
    can_be_blocked = forms.YesNoSwitch(
        label=_("Can be blocked by other users"),
        initial=0)
    can_see_users_name_history = CAN_SEE_USER_NAME_HISTORY
    can_see_ban_details = CAN_SEE_BAN_DETAILS
    can_see_users_emails = forms.YesNoSwitch(
        label=_("Can see members e-mails"))
    can_see_users_ips = forms.YesNoSwitch(
        label=_("Can see members IPs"))
    can_see_hidden_users = forms.YesNoSwitch(
        label=_("Can see members that hide their presence"))


def change_permissions_form(role):
    if isinstance(role, Role):
        if role.special_role == 'anonymous':
            return LimitedPermissionsForm
        else:
            return PermissionsForm
    else:
        return None


"""
ACL Builder
"""
def build_acl(acl, roles, key_name):
    new_acl = {
        'can_search_users': 0,
        'can_follow_users': 1,
        'can_be_blocked': 1,
        'can_see_users_name_history': 0,
        'can_see_ban_details': 0,
        'can_see_users_emails': 0,
        'can_see_users_ips': 0,
        'can_see_hidden_users': 0,
    }
    new_acl.update(acl)

    return algebra.sum_acls(
            new_acl, roles=roles, key=key_name,
            can_search_users=algebra.greater,
            can_follow_users=algebra.greater,
            can_be_blocked=algebra.lower,
            can_see_users_name_history=algebra.greater,
            can_see_ban_details=algebra.greater,
            can_see_users_emails=algebra.greater,
            can_see_users_ips=algebra.greater,
            can_see_hidden_users=algebra.greater
            )


"""
ACL's for targets
"""
@require_target_type(get_user_model())
def add_acl_to_target(user, target):
    target_acl = target.acl_

    target_acl['can_have_attitude'] = False
    target_acl['can_follow'] = can_follow_user(user, target)
    target_acl['can_block'] = can_block_user(user, target)

    mod_permissions = (
        'can_have_attitude',
        'can_follow',
        'can_block',
    )

    for permission in mod_permissions:
        if target_acl[permission]:
            target_acl['can_have_attitude'] = True
            break


"""
ACL tests
"""
@authenticated_only
def allow_follow_user(user, target):
    if not user.acl['can_follow_users']:
        raise PermissionDenied(_("You can't follow other users."))
    if user.pk == target.pk:
        raise PermissionDenied(_("You can't add yourself to followed."))
can_follow_user = return_boolean(allow_follow_user)


@authenticated_only
def allow_block_user(user, target):
    if target.is_staff or target.is_superuser:
        raise PermissionDenied(_("You can't block administrators."))
    if user.pk == target.pk:
        raise PermissionDenied(_("You can't block yourself."))
    if not target.acl['can_be_blocked'] or target.is_superuser:
        message = _("%(user)s can't be blocked.") % {'user': target.username}
        raise PermissionDenied(message)
can_block_user = return_boolean(allow_block_user)
