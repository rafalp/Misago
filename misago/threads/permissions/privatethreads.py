from django.utils.translation import ugettext_lazy as _

from misago.acl import add_acl, algebra
from misago.acl.decorators import return_boolean
from misago.acl.models import Role
from misago.core import forms


__all__ = [
]


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("Private threads")
    can_use_private_threads = forms.YesNoSwitch(
        label=_("Can use private threads"))
    can_start_private_threads = forms.YesNoSwitch(
        label=_("Can start private threads"))
    max_private_thread_participants = forms.IntegerField(
        label=_("Max number of users invited to private thread"),
        help_text=_("Enter 0 to don't limit number of participants."),
        initial=3,
        min_value=0)
    can_add_everyone_to_private_threads = forms.YesNoSwitch(
        label=_("Can add everyone to threads"),
        help_text=_("Allows user to add users that are "
                    "blocking him to private threads."))
    can_report_private_threads = forms.YesNoSwitch(
        label=_("Can report private threads"),
        help_text=_("Allows user to report private threads they are "
                    "participating in, making them accessible to moderators."))
    can_moderate_private_threads = forms.YesNoSwitch(
        label=_("Can moderate private threads"),
        help_text=_("Allows user to read, reply, edit and delete "
                "content in reported private threads."))


def change_permissions_form(role):
    if isinstance(role, Role) and role.special_role != 'anonymous':
        return PermissionsForm
    else:
        return None


"""
ACL Builder
"""
def build_acl(acl, roles, key_name):
    new_acl = {
        'can_use_private_threads': 0,
        'can_start_private_threads': 0,
        'max_private_thread_participants': 3,
        'can_add_everyone_to_private_threads': 0,
        'can_report_private_threads': 0,
        'can_moderate_private_threads': 0,
    }

    new_acl.update(acl)

    algebra.sum_acls(new_acl, roles=roles, key=key_name,
        can_use_private_threads=algebra.greater,
        can_start_private_threads=algebra.greater,
        max_private_thread_participants=algebra.greater_or_zero,
        can_add_everyone_to_private_threads=algebra.greater,
        can_report_private_threads=algebra.greater,
        can_moderate_private_threads=algebra.greater
    )

    return new_acl
