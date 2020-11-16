from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

from ...acl import algebra
from ...acl.decorators import return_boolean
from ...acl.models import Role
from ...admin.forms import YesNoSwitch
from .decorators import authenticated_only

__all__ = [
    "allow_browse_users_list",
    "can_browse_users_list",
    "allow_follow_user",
    "can_follow_user",
    "allow_block_user",
    "can_block_user",
    "allow_see_ban_details",
    "can_see_ban_details",
]

CAN_BROWSE_USERS_LIST = YesNoSwitch(label=_("Can browse users list"), initial=1)
CAN_SEARCH_USERS = YesNoSwitch(label=_("Can search user profiles"), initial=1)
CAN_SEE_USER_NAME_HISTORY = YesNoSwitch(label=_("Can see other members name history"))
CAN_SEE_DETAILS = YesNoSwitch(
    label=_("Can see members bans details"),
    help_text=_(
        "Allows users with this permission to see user and staff ban messages."
    ),
)


class LimitedPermissionsForm(forms.Form):
    legend = _("User profiles")

    can_browse_users_list = CAN_BROWSE_USERS_LIST
    can_search_users = CAN_SEARCH_USERS
    can_see_users_name_history = CAN_SEE_USER_NAME_HISTORY
    can_see_ban_details = CAN_SEE_DETAILS


class PermissionsForm(LimitedPermissionsForm):
    can_browse_users_list = CAN_BROWSE_USERS_LIST
    can_search_users = CAN_SEARCH_USERS
    can_follow_users = YesNoSwitch(label=_("Can follow other users"), initial=1)
    can_be_blocked = YesNoSwitch(label=_("Can be blocked by other users"), initial=0)
    can_see_users_name_history = CAN_SEE_USER_NAME_HISTORY
    can_see_ban_details = CAN_SEE_DETAILS
    can_see_users_emails = YesNoSwitch(label=_("Can see members e-mails"))
    can_see_users_ips = YesNoSwitch(label=_("Can see members IPs"))
    can_see_hidden_users = YesNoSwitch(
        label=_("Can see members that hide their presence")
    )


def change_permissions_form(role):
    if isinstance(role, Role):
        if role.special_role == "anonymous":
            return LimitedPermissionsForm
        return PermissionsForm


def build_acl(acl, roles, key_name):
    new_acl = {
        "can_browse_users_list": 0,
        "can_search_users": 0,
        "can_follow_users": 0,
        "can_be_blocked": 1,
        "can_see_users_name_history": 0,
        "can_see_ban_details": 0,
        "can_see_users_emails": 0,
        "can_see_users_ips": 0,
        "can_see_hidden_users": 0,
    }
    new_acl.update(acl)

    return algebra.sum_acls(
        new_acl,
        roles=roles,
        key=key_name,
        can_browse_users_list=algebra.greater,
        can_search_users=algebra.greater,
        can_follow_users=algebra.greater,
        can_be_blocked=algebra.lower,
        can_see_users_name_history=algebra.greater,
        can_see_ban_details=algebra.greater,
        can_see_users_emails=algebra.greater,
        can_see_users_ips=algebra.greater,
        can_see_hidden_users=algebra.greater,
    )


def add_acl_to_user(user_acl, target):
    target.acl["can_have_attitude"] = False
    target.acl["can_follow"] = can_follow_user(user_acl, target)
    target.acl["can_block"] = can_block_user(user_acl, target)

    mod_permissions = ("can_have_attitude", "can_follow", "can_block")

    for permission in mod_permissions:
        if target.acl[permission]:
            target.acl["can_have_attitude"] = True
            break


def register_with(registry):
    registry.acl_annotator(get_user_model(), add_acl_to_user)


def allow_browse_users_list(user_acl):
    if not user_acl["can_browse_users_list"]:
        raise PermissionDenied(_("You can't browse users list."))


can_browse_users_list = return_boolean(allow_browse_users_list)


@authenticated_only
def allow_follow_user(user_acl, target):
    if not user_acl["can_follow_users"]:
        raise PermissionDenied(_("You can't follow other users."))
    if user_acl["user_id"] == target.id:
        raise PermissionDenied(_("You can't add yourself to followed."))


can_follow_user = return_boolean(allow_follow_user)


@authenticated_only
def allow_block_user(user_acl, target):
    if target.is_staff or target.is_superuser:
        raise PermissionDenied(_("You can't block administrators."))
    if user_acl["user_id"] == target.id:
        raise PermissionDenied(_("You can't block yourself."))
    # FIXME: check if user has "can be blocked" permission


can_block_user = return_boolean(allow_block_user)


@authenticated_only
def allow_see_ban_details(user_acl, target):
    if not user_acl["can_see_ban_details"]:
        raise PermissionDenied(_("You can't see users bans details."))


can_see_ban_details = return_boolean(allow_see_ban_details)
