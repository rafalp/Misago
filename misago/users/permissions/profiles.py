from django.utils.translation import ugettext_lazy as _

from misago.acl import algebra
from misago.acl.models import Role
from misago.core import forms


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("User profiles")

    can_search_users = forms.YesNoSwitch(
        label=_("Can search user profiles"),
        initial=1)
    can_see_users_name_history = forms.YesNoSwitch(
        label=_("Can see other members name history"))
    can_see_ban_details = forms.YesNoSwitch(
        label=_("Can see members bans details"),
        help_text=_("Allows users with this permission to see user and "
                    "staff ban messages."))
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
    new_acl = {
        'can_search_users': 0,
        'can_see_users_name_history': 0,
        'can_see_ban_details': 0,
        'can_see_users_emails': 0,
        'can_see_users_ips': 0,
        'can_see_hidden_users': 0,
    }
    new_acl.update(acl)

    return algebra.sum_acls(
            new_acl, roles=roles, key=key_name,
            can_see_users_name_history=algebra.greater,
            can_see_ban_details=algebra.greater,
            can_search_users=algebra.greater,
            can_see_users_emails=algebra.greater,
            can_see_users_ips=algebra.greater,
            can_see_hidden_users=algebra.greater
            )
