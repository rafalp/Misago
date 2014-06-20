from django.utils.translation import ugettext_lazy as _
from misago.acl.models import Role
from misago.core import forms


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("User profiles")
    can_search_users = forms.YesNoSwitch(
        label=_("Can search user profiles"),
        initial=True)
    can_see_users_emails = forms.YesNoSwitch(
        label=_("Can see members e-mails"))
    can_see_users_ips = forms.YesNoSwitch(
        label=_("Can see members IPs"))
    can_see_hidden_users = forms.YesNoSwitch(
        label=_("Can see members that hide their presence"))


def change_permissions_form(role):
    if isinstance(role, Role):
        return PermissionsForm
    else:
        return None


"""
ACL Builder
"""
def build_acl(acl, roles, key_name):
    pass
