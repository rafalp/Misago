from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from misago.acl import add_acl, algebra
from misago.acl.decorators import return_boolean
from misago.acl.models import Role
from misago.core import forms


__all__ = [
    'allow_use_private_threads',
    'can_use_private_threads',
    'allow_message_user',
    'can_message_user',
    'exclude_invisible_private_threads',
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


"""
ACL tests
"""
def allow_use_private_threads(user):
    if user.is_anonymous():
        raise PermissionDenied(_("Unsigned members can't use "
                                 "private threads system."))
    if not user.acl['can_use_private_threads']:
        raise PermissionDenied(_("You can't use private threads system."))
can_use_private_threads = return_boolean(allow_use_private_threads)



def allow_message_user(user, target):
    allow_use_private_threads(user)

    if user == target:
        raise PermissionDenied(_("You can't message yourself."))

    if not user.acl['can_start_private_threads']:
        raise PermissionDenied(_("You can't start private threads."))

    if user.acl['can_add_everyone_to_private_threads']:
        return None

    message_format = {'user': user.username}

    if user.acl['can_be_blocked'] and target.is_blocking(user):
        message = _("%(user)s is blocking you.")
        raise PermissionDenied(message % message_format)

    if target.can_be_messaged_by_nobody:
        message = _("%(user)s is not allowing invitations to private threads.")
        raise PermissionDenied(message % message_format)

    if target.can_be_messaged_by_followed and not target.is_following(user):
        message = _("%(user)s is allowing invitations to private "
                    "threads only from followed users.")
        raise PermissionDenied(message % message_format)
can_message_user = return_boolean(allow_message_user)


"""
Queryset helpers
"""
def exclude_invisible_private_threads(queryset, user):
    if user.acl['can_moderate_private_threads']:
        see_participating = Q(participants=user)
        see_reported = Q(has_reported_posts=True)
        return queryset.filter(see_reported | see_participating)
    else:
        return queryset.filter(participants=user)
