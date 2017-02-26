from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.template.defaultfilters import date as format_date
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from misago.acl import algebra
from misago.acl.decorators import return_boolean
from misago.acl.models import Role
from misago.core.forms import YesNoSwitch
from misago.users.bans import get_user_ban


__all__ = [
    'allow_rename_user',
    'can_rename_user',
    'allow_moderate_avatar',
    'can_moderate_avatar',
    'allow_moderate_signature',
    'can_moderate_signature',
    'allow_ban_user',
    'can_ban_user',
    'allow_lift_ban',
    'can_lift_ban',
]


class PermissionsForm(forms.Form):
    legend = _("Users moderation")

    can_rename_users = YesNoSwitch(label=_("Can rename users"))
    can_moderate_avatars = YesNoSwitch(label=_("Can moderate avatars"))
    can_moderate_signatures = YesNoSwitch(label=_("Can moderate signatures"))
    can_ban_users = YesNoSwitch(label=_("Can ban users"))
    max_ban_length = forms.IntegerField(
        label=_("Max length, in days, of imposed ban"),
        help_text=_("Enter zero to let moderators impose permanent bans."),
        min_value=0,
        initial=0,
    )
    can_lift_bans = YesNoSwitch(label=_("Can lift bans"))
    max_lifted_ban_length = forms.IntegerField(
        label=_("Max length, in days, of lifted ban"),
        help_text=_("Enter zero to let moderators lift permanent bans."),
        min_value=0,
        initial=0,
    )


def change_permissions_form(role):
    if isinstance(role, Role) and role.special_role != 'anonymous':
        return PermissionsForm
    else:
        return None


def build_acl(acl, roles, key_name):
    new_acl = {
        'can_rename_users': 0,
        'can_moderate_avatars': 0,
        'can_moderate_signatures': 0,
        'can_ban_users': 0,
        'max_ban_length': 2,
        'can_lift_bans': 0,
        'max_lifted_ban_length': 2,
    }
    new_acl.update(acl)

    return algebra.sum_acls(
        new_acl,
        roles=roles,
        key=key_name,
        can_rename_users=algebra.greater,
        can_moderate_avatars=algebra.greater,
        can_moderate_signatures=algebra.greater,
        can_ban_users=algebra.greater,
        max_ban_length=algebra.greater_or_zero,
        can_lift_bans=algebra.greater,
        max_lifted_ban_length=algebra.greater_or_zero,
    )


def add_acl_to_user(user, target):
    target.acl['can_rename'] = can_rename_user(user, target)
    target.acl['can_moderate_avatar'] = can_moderate_avatar(user, target)
    target.acl['can_moderate_signature'] = can_moderate_signature(user, target)
    target.acl['can_ban'] = can_ban_user(user, target)
    target.acl['max_ban_length'] = user.acl_cache['max_ban_length']
    target.acl['can_lift_ban'] = can_lift_ban(user, target)

    mod_permissions = [
        'can_rename',
        'can_moderate_avatar',
        'can_moderate_signature',
        'can_ban',
    ]

    for permission in mod_permissions:
        if target.acl[permission]:
            target.acl['can_moderate'] = True
            break


def register_with(registry):
    registry.acl_annotator(get_user_model(), add_acl_to_user)


def allow_rename_user(user, target):
    if not user.acl_cache['can_rename_users']:
        raise PermissionDenied(_("You can't rename users."))
    if not user.is_superuser and (target.is_staff or target.is_superuser):
        raise PermissionDenied(_("You can't rename administrators."))


can_rename_user = return_boolean(allow_rename_user)


def allow_moderate_avatar(user, target):
    if not user.acl_cache['can_moderate_avatars']:
        raise PermissionDenied(_("You can't moderate avatars."))
    if not user.is_superuser and (target.is_staff or target.is_superuser):
        raise PermissionDenied(_("You can't moderate administrators avatars."))


can_moderate_avatar = return_boolean(allow_moderate_avatar)


def allow_moderate_signature(user, target):
    if not user.acl_cache['can_moderate_signatures']:
        raise PermissionDenied(_("You can't moderate signatures."))
    if not user.is_superuser and (target.is_staff or target.is_superuser):
        message = _("You can't moderate administrators signatures.")
        raise PermissionDenied(message)


can_moderate_signature = return_boolean(allow_moderate_signature)


def allow_ban_user(user, target):
    if not user.acl_cache['can_ban_users']:
        raise PermissionDenied(_("You can't ban users."))
    if target.is_staff or target.is_superuser:
        raise PermissionDenied(_("You can't ban administrators."))


can_ban_user = return_boolean(allow_ban_user)


def allow_lift_ban(user, target):
    if not user.acl_cache['can_lift_bans']:
        raise PermissionDenied(_("You can't lift bans."))
    ban = get_user_ban(target)
    if not ban:
        raise PermissionDenied(_("This user is not banned."))
    if user.acl_cache['max_lifted_ban_length']:
        expiration_limit = timedelta(days=user.acl_cache['max_lifted_ban_length'])
        lift_cutoff = (timezone.now() + expiration_limit).date()
        if not ban.valid_until:
            raise PermissionDenied(_("You can't lift permanent bans."))
        elif ban.valid_until > lift_cutoff:
            message = _("You can't lift bans that expire after %(expiration)s.")
            raise PermissionDenied(message % {'expiration': format_date(lift_cutoff)})


can_lift_ban = return_boolean(allow_lift_ban)
