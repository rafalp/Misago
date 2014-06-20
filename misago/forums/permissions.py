from django.utils.translation import ugettext_lazy as _
from misago.core import forms
from misago.forums.models import ForumRole


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("Forum access")
    can_see = forms.YesNoSwitch(label=_("Can see forum"))
    can_browse = forms.YesNoSwitch(label=_("Can see forum contents"))


def change_permissions_form(role):
    if isinstance(role, ForumRole):
        return PermissionsForm
    else:
        return None


"""
ACL Builder
"""
def build_acl(acl, roles, key_name):
    pass
