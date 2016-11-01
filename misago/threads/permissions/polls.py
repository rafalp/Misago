from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _, ungettext

from misago.acl import algebra
from misago.acl.decorators import return_boolean
from misago.acl.models import Role
from misago.core import forms

from ..models import Poll, Thread


"""
Admin Permissions Forms
"""
class RolePermissionsForm(forms.Form):
    legend = _("Polls")

    can_start_polls = forms.TypedChoiceField(
        label=_("Can start polls"),
        coerce=int,
        initial=0,
        choices=(
            (0, _("No")),
            (1, _("Own threads")),
            (2, _("All threads"))
        )
    )
    can_edit_polls = forms.TypedChoiceField(
        label=_("Can edit polls"),
        coerce=int,
        initial=0,
        choices=(
            (0, _("No")),
            (1, _("Own polls")),
            (2, _("All polls"))
        )
    )
    can_delete_polls = forms.TypedChoiceField(
        label=_("Can edit polls"),
        coerce=int,
        initial=0,
        choices=(
            (0, _("No")),
            (1, _("Own polls")),
            (2, _("All polls"))
        )
    )
    poll_edit_time = forms.IntegerField(
        label=_("Time limit for own polls edits, in minutes"),
        help_text=_("Enter 0 to don't limit time for editing own polls."),
        initial=0,
        min_value=0
    )
    can_always_see_poll_voters = forms.YesNoSwitch(
        label=_("Can always see polls voters"),
        help_text=_("Allows users to see who voted in poll even if poll votes are secret.")
    )


def change_permissions_form(role):
    if isinstance(role, Role) and role.special_role != 'anonymous':
        return RolePermissionsForm
    else:
        return None


"""
ACL Builder
"""
def build_acl(acl, roles, key_name):
    acl.update({
        'can_start_polls': 0,
        'can_edit_polls': 0,
        'can_delete_polls': 0,
        'poll_edit_time': 0,
        'can_always_see_poll_voters': 0
    })

    return algebra.sum_acls(acl, roles=roles, key=key_name,
        can_start_polls=algebra.greater,
        can_edit_polls=algebra.greater,
        can_delete_polls=algebra.greater,
        poll_edit_time=algebra.greater_or_zero,
        can_always_see_poll_voters=algebra.greater
    )


"""
ACL's for targets
"""
def add_acl_to_poll(user, poll):
    poll.acl.update({
        'can_edit': False,
        'can_delete': False,
    })


def add_acl_to_thread(user, thread):
    thread.acl.update({
        'can_start_poll': can_start_poll(user, thread)
    })


def register_with(registry):
    registry.acl_annotator(Poll, add_acl_to_poll)
    registry.acl_annotator(Thread, add_acl_to_thread)


"""
ACL tests
"""
def allow_start_poll(user, target):
    if user.is_anonymous():
        raise PermissionDenied(_("You have to sign in to start polls."))

    category_acl = user.acl['categories'].get(target.category_id, {
        'can_close_threads': False,
    })

    if not user.acl.get('can_start_polls'):
        raise PermissionDenied(_("You can't start polls."))
    if user.acl.get('can_start_polls') < 2 and user.pk != target.starter_id:
        raise PermissionDenied(_("You can't start polls in other users threads."))

    if not category_acl.get('can_close_threads'):
        if target.category.is_closed:
            raise PermissionDenied(_("This category is closed. You can't start polls in it."))
        if target.is_closed:
            raise PermissionDenied(_("This thread is closed. You can't start polls in it."))
    try:
        if target.poll:
            raise PermissionDenied(_("There's already a poll in this thread."))
    except Poll.DoesNotExist:
        pass
can_start_poll = return_boolean(allow_start_poll)
