from django.utils.translation import ugettext_lazy as _
from misago.acl.models import Role
from misago.core import forms


DEFAULT_PERMISSIONS = {
    'name_changes_allowed': 1,
    'changes_expire': 0,
    'can_use_signature': True,
    'allow_signature_links': True,
    'allow_signature_images': False,
}


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("Account settings")
    name_changes_allowed = forms.IntegerField(
        label=_("Allowed username changes number"),
        min_value=0,
        initial=1)
    changes_expire = forms.IntegerField(
        label=_("Don't count username changes older than"),
        help_text=_("Number of days since name change that makes that change no longer count to limit. Enter zero to make all changes count."),
        min_value=0,
        initial=0)
    can_use_signature = forms.YesNoSwitch(
        label=_("Can have signature"),
        initial=True)
    allow_signature_links = forms.YesNoSwitch(
        label=_("Can put links in signature"),
        initial=True)
    allow_signature_images = forms.YesNoSwitch(
        label=_("Can put images in signature"))


def change_permissions_form(role):
    if isinstance(role, Role):
        return PermissionsForm
    else:
        return None


"""
ACL Builder
"""
def build_acl(acl, roles):
    pass
