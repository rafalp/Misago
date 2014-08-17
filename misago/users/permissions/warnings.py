from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from misago.acl import algebra
from misago.acl.decorators import return_boolean
from misago.acl.models import Role
from misago.core import forms

from misago.users.models import UserWarning
from misago.users.permissions.decorators import authenticated_only


"""
Admin Permissions Form
"""
NO_OWNED_ALL = ((0, _("No")), (1, _("Owned")), (2, _("All")))


class LimitedPermissionsForm(forms.Form):
    legend = _("Warnings")

    can_see_other_users_warnings = forms.YesNoSwitch(
        label=_("Can see other users warnings"))


class PermissionsForm(LimitedPermissionsForm):
    can_warn_users = forms.YesNoSwitch(label=_("Can warn users"))
    can_be_warned = forms.YesNoSwitch(label=_("Can be warned"), initial=False)
    can_cancel_warnings = forms.TypedChoiceField(
        label=_("Can cancel warnings"),
        coerce=int,
        choices=NO_OWNED_ALL,
        initial=0)
    can_delete_warnings = forms.TypedChoiceField(
        label=_("Can delete warnings"),
        coerce=int,
        choices=NO_OWNED_ALL,
        initial=0)


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
        'can_see_other_users_warnings': 0,
        'can_warn_users': 0,
        'can_cancel_warnings': 0,
        'can_delete_warnings': 0,
        'can_be_warned': 1,
    }
    new_acl.update(acl)

    return algebra.sum_acls(new_acl, roles=roles, key=key_name,
        can_see_other_users_warnings=algebra.greater,
        can_warn_users=algebra.greater,
        can_cancel_warnings=algebra.greater,
        can_delete_warnings=algebra.greater,
        can_be_warned=algebra.lower
    )


"""
ACL's for targets
"""
def add_acl_to_target(user, target):
    if isinstance(target, get_user_model()):
        add_acl_to_user(user, target)
    elif isinstance(target, UserWarning):
        add_acl_to_warning(user, target)


def add_acl_to_user(user, target):
    target_acl = target.acl_

    target_acl['can_see_warnings'] = can_see_warnings(user, target)
    target_acl['can_warn'] = can_warn_user(user, target)
    target_acl['can_cancel_warnings'] = False
    target_acl['can_delete_warnings'] = False

    if target_acl['can_warn']:
        target_acl['can_moderate'] = True


def add_acl_to_warning(user, target):
    target.acl['can_cancel'] = can_cancel_warning(user, target)
    target.acl['can_delete'] = can_delete_warning(user, target)

    can_moderate = target.acl['can_cancel'] or target.acl['can_delete']
    target.acl['can_moderate'] = can_moderate


"""
ACL tests
"""
def allow_see_warnings(user, target):
    if user.is_authenticated() and user.pk == target.pk:
        return None
    if not user.acl['can_see_other_users_warnings']:
        raise PermissionDenied(_("You can't see other users warnings."))
can_see_warnings = return_boolean(allow_see_warnings)


@authenticated_only
def allow_warn_user(user, target):
    if not user.acl['can_warn_users']:
        raise PermissionDenied(_("You can't warn users."))
    if not user.is_superuser and (target.is_staff or target.is_superuser):
        raise PermissionDenied(_("You can't warn administrators."))
    if not target.acl['can_be_warned']:
        message = _("%(user)s can't be warned.")
        raise PermissionDenied(message % {'user': target.username})
can_warn_user = return_boolean(allow_warn_user)


@authenticated_only
def allow_cancel_warning(user, target):
    if user.is_anonymous() or not user.acl['can_cancel_warnings']:
        raise PermissionDenied(_("You can't cancel warnings."))
    if user.acl['can_cancel_warnings'] == 1:
        if target.giver_id != user.pk:
            message = _("You can't cancel warnings issued by other users.")
            raise PermissionDenied(message)
    if target.is_canceled:
        raise PermissionDenied(_("This warning is already canceled."))
can_cancel_warning = return_boolean(allow_cancel_warning)


@authenticated_only
def allow_delete_warning(user, target):
    if user.is_anonymous() or not user.acl['can_delete_warnings']:
        raise PermissionDenied(_("You can't delete warnings."))
    if user.acl['can_delete_warnings'] == 1:
        if target.giver_id != user.pk:
            message = _("You can't delete warnings issued by other users.")
            raise PermissionDenied(message)
can_delete_warning = return_boolean(allow_delete_warning)
