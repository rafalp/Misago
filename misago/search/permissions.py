from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from misago.acl import algebra
from misago.acl.models import Role
from misago.core import forms


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("Search")

    can_search = forms.YesNoSwitch(
        label=_("Can search site"),
        initial=1
    )


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
        'can_search': 0
    }
    new_acl.update(acl)

    return algebra.sum_acls(new_acl, roles=roles, key=key_name,
        can_search=algebra.greater
    )
