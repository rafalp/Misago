from django import forms
from django.utils.translation import pgettext_lazy

from ..acl import algebra
from ..acl.models import Role
from ..admin.forms import YesNoSwitch


class PermissionsForm(forms.Form):
    legend = pgettext_lazy("search permission", "Search")

    can_search = YesNoSwitch(
        label=pgettext_lazy("search permission", "Can search site"), initial=1
    )


def change_permissions_form(role):
    if isinstance(role, Role):
        return PermissionsForm


def build_acl(acl, roles, key_name):
    new_acl = {"can_search": 0}
    new_acl.update(acl)

    return algebra.sum_acls(
        new_acl, roles=roles, key=key_name, can_search=algebra.greater
    )
