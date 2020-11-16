from django import forms
from django.utils.translation import gettext_lazy as _

from ..acl import algebra
from ..acl.models import Role
from ..admin.forms import YesNoSwitch


class PermissionsForm(forms.Form):
    legend = _("Search")

    can_search = YesNoSwitch(label=_("Can search site"), initial=1)


def change_permissions_form(role):
    if isinstance(role, Role):
        return PermissionsForm


def build_acl(acl, roles, key_name):
    new_acl = {"can_search": 0}
    new_acl.update(acl)

    return algebra.sum_acls(
        new_acl, roles=roles, key=key_name, can_search=algebra.greater
    )
