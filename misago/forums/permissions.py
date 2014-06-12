from django.utils.translation import ugettext_lazy as _
from misago.core import forms
from misago.forums.models import ForumRole


DEFAULT_PERMISSIONS = {
    'can_see': False,
    'can_browse': False
}


class PermissionsForm(forms.Form):
    legend = _("Forum access")
    can_see = forms.YesNoSwitch(label=_("Can see forum"))
    can_browse = forms.YesNoSwitch(label=_("Can see forum contents"))


def change_permissions_form(role):
    if role.__class__ == ForumRole:
        return PermissionsForm
    else:
        return None
