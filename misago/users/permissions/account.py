from django import forms
from django.utils.translation import gettext_lazy as _

from ...acl import algebra
from ...acl.models import Role
from ...admin.forms import YesNoSwitch


class PermissionsForm(forms.Form):
    legend = _("Account settings")

    name_changes_allowed = forms.IntegerField(
        label=_("Allowed username changes number"), min_value=0, initial=1
    )
    name_changes_expire = forms.IntegerField(
        label=_("Don't count username changes older than"),
        help_text=_(
            "Number of days since name change that makes "
            "that change no longer count to limit. Enter "
            "zero to make all changes count."
        ),
        min_value=0,
        initial=0,
    )
    can_have_signature = YesNoSwitch(label=_("Can have signature"))
    allow_signature_links = YesNoSwitch(label=_("Can put links in signature"))
    allow_signature_images = YesNoSwitch(label=_("Can put images in signature"))
    allow_signature_blocks = YesNoSwitch(
        label=_("Can use text blocks in signature"),
        help_text=_(
            "Controls whether or not users can put quote, code, "
            "spoiler blocks and horizontal lines in signatures."
        ),
    )


def change_permissions_form(role):
    if isinstance(role, Role) and role.special_role != "anonymous":
        return PermissionsForm


def build_acl(acl, roles, key_name):
    new_acl = {
        "name_changes_allowed": 0,
        "name_changes_expire": 0,
        "can_have_signature": 0,
        "allow_signature_links": 0,
        "allow_signature_images": 0,
        "allow_signature_blocks": 0,
    }
    new_acl.update(acl)

    return algebra.sum_acls(
        new_acl,
        roles=roles,
        key=key_name,
        name_changes_allowed=algebra.greater,
        name_changes_expire=algebra.lower_non_zero,
        can_have_signature=algebra.greater,
        allow_signature_links=algebra.greater,
        allow_signature_images=algebra.greater,
        allow_signature_blocks=algebra.greater,
    )
