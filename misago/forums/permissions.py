from django.utils.translation import ugettext_lazy as _
from misago.acl.models import ForumRole
from misago.core import forms


class PermissionsForm(forms.Form):
    legend = _("Destroying user accounts")
    can_see_forum = forms.YesNoSwitch(label=_("Can see forum"))
    can_browse_forum = forms.YesNoSwitch(label=_("Can see forum contents"))


def change_permissions_form(role):
    if role.__class__ == ForumRole:
        return PermissionsForm
    else:
        return None
