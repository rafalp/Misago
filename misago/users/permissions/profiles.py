from django.utils.translation import ugettext_lazy as _
from misago.acl.models import Role
from misago.core import forms


class PermissionsForm(forms.Form):
    legend = _("User profiles")
    can_search_users = forms.YesNoSwitch(
        label=_("Can search user profiles"))
    can_see_users_emails = forms.YesNoSwitch(
        label=_("Can see members e-mail's"))
    can_see_users_trails = forms.YesNoSwitch(
        label=_("Can see members ip's and user-agents"))
    can_see_hidden_users = forms.YesNoSwitch(
        label=_("Can see members that hide their presence"))



def change_permissions_form(role):
    if role.__class__ == Role:
        return PermissionsForm
    else:
        return None
