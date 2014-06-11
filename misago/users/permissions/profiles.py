from django.utils.translation import ugettext_lazy as _
from misago.acl.models import Role
from misago.core import forms


DEFAULT_PERMISSIONS = {
    'can_search_users': True,
    'can_see_users_emails': False,
    'can_see_users_ips': False,
    'can_see_hidden_users': False,
}


class PermissionsForm(forms.Form):
    legend = _("User profiles")
    can_search_users = forms.YesNoSwitch(
        label=_("Can search user profiles"))
    can_see_users_emails = forms.YesNoSwitch(
        label=_("Can see members e-mails"))
    can_see_users_ips = forms.YesNoSwitch(
        label=_("Can see members IPs"))
    can_see_hidden_users = forms.YesNoSwitch(
        label=_("Can see members that hide their presence"))


def change_permissions_form(role):
    if role.__class__ == Role:
        return PermissionsForm
    else:
        return None
