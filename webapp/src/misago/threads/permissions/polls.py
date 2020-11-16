from django import forms
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from ...acl import algebra
from ...acl.decorators import return_boolean
from ...acl.models import Role
from ...admin.forms import YesNoSwitch
from ..models import Poll, Thread

__all__ = [
    "allow_start_poll",
    "can_start_poll",
    "allow_edit_poll",
    "can_edit_poll",
    "allow_delete_poll",
    "can_delete_poll",
    "allow_vote_poll",
    "can_vote_poll",
    "allow_see_poll_votes",
    "can_see_poll_votes",
]


class RolePermissionsForm(forms.Form):
    legend = _("Polls")

    can_start_polls = forms.TypedChoiceField(
        label=_("Can start polls"),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Own threads")), (2, _("All threads"))],
    )
    can_edit_polls = forms.TypedChoiceField(
        label=_("Can edit polls"),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Own polls")), (2, _("All polls"))],
    )
    can_delete_polls = forms.TypedChoiceField(
        label=_("Can delete polls"),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Own polls")), (2, _("All polls"))],
    )
    poll_edit_time = forms.IntegerField(
        label=_("Time limit for own polls edits, in minutes"),
        help_text=_("Enter 0 to don't limit time for editing own polls."),
        initial=0,
        min_value=0,
    )
    can_always_see_poll_voters = YesNoSwitch(
        label=_("Can always see polls voters"),
        help_text=_(
            "Allows users to see who voted in poll even if poll votes are secret."
        ),
    )


def change_permissions_form(role):
    if isinstance(role, Role) and role.special_role != "anonymous":
        return RolePermissionsForm


def build_acl(acl, roles, key_name):
    acl.update(
        {
            "can_start_polls": 0,
            "can_edit_polls": 0,
            "can_delete_polls": 0,
            "poll_edit_time": 0,
            "can_always_see_poll_voters": 0,
        }
    )

    return algebra.sum_acls(
        acl,
        roles=roles,
        key=key_name,
        can_start_polls=algebra.greater,
        can_edit_polls=algebra.greater,
        can_delete_polls=algebra.greater,
        poll_edit_time=algebra.greater_or_zero,
        can_always_see_poll_voters=algebra.greater,
    )


def add_acl_to_poll(user_acl, poll):
    poll.acl.update(
        {
            "can_vote": can_vote_poll(user_acl, poll),
            "can_edit": can_edit_poll(user_acl, poll),
            "can_delete": can_delete_poll(user_acl, poll),
            "can_see_votes": can_see_poll_votes(user_acl, poll),
        }
    )


def add_acl_to_thread(user_acl, thread):
    thread.acl.update({"can_start_poll": can_start_poll(user_acl, thread)})


def register_with(registry):
    registry.acl_annotator(Poll, add_acl_to_poll)
    registry.acl_annotator(Thread, add_acl_to_thread)


def allow_start_poll(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to start polls."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_close_threads": False}
    )

    if not user_acl.get("can_start_polls"):
        raise PermissionDenied(_("You can't start polls."))
    if user_acl.get("can_start_polls") < 2 and user_acl["user_id"] != target.starter_id:
        raise PermissionDenied(_("You can't start polls in other users threads."))

    if not category_acl.get("can_close_threads"):
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't start polls in it.")
            )
        if target.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't start polls in it.")
            )


can_start_poll = return_boolean(allow_start_poll)


def allow_edit_poll(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to edit polls."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_close_threads": False}
    )

    if not user_acl.get("can_edit_polls"):
        raise PermissionDenied(_("You can't edit polls."))

    if user_acl.get("can_edit_polls") < 2:
        if user_acl["user_id"] != target.poster_id:
            raise PermissionDenied(
                _("You can't edit other users polls in this category.")
            )
        if not has_time_to_edit_poll(user_acl, target):
            message = ngettext(
                "You can't edit polls that are older than %(minutes)s minute.",
                "You can't edit polls that are older than %(minutes)s minutes.",
                user_acl["poll_edit_time"],
            )
            raise PermissionDenied(message % {"minutes": user_acl["poll_edit_time"]})

        if target.is_over:
            raise PermissionDenied(_("This poll is over. You can't edit it."))

    if not category_acl.get("can_close_threads"):
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't edit polls in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't edit polls in it.")
            )


can_edit_poll = return_boolean(allow_edit_poll)


def allow_delete_poll(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to delete polls."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_close_threads": False}
    )

    if not user_acl.get("can_delete_polls"):
        raise PermissionDenied(_("You can't delete polls."))

    if user_acl.get("can_delete_polls") < 2:
        if user_acl["user_id"] != target.poster_id:
            raise PermissionDenied(
                _("You can't delete other users polls in this category.")
            )
        if not has_time_to_edit_poll(user_acl, target):
            message = ngettext(
                "You can't delete polls that are older than %(minutes)s minute.",
                "You can't delete polls that are older than %(minutes)s minutes.",
                user_acl["poll_edit_time"],
            )
            raise PermissionDenied(message % {"minutes": user_acl["poll_edit_time"]})
        if target.is_over:
            raise PermissionDenied(_("This poll is over. You can't delete it."))

    if not category_acl.get("can_close_threads"):
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't delete polls in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't delete polls in it.")
            )


can_delete_poll = return_boolean(allow_delete_poll)


def allow_vote_poll(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to vote in polls."))

    if target.has_selected_choices and not target.allow_revotes:
        raise PermissionDenied(_("You have already voted in this poll."))
    if target.is_over:
        raise PermissionDenied(_("This poll is over. You can't vote in it."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_close_threads": False}
    )

    if not category_acl.get("can_close_threads"):
        if target.category.is_closed:
            raise PermissionDenied(_("This category is closed. You can't vote in it."))
        if target.thread.is_closed:
            raise PermissionDenied(_("This thread is closed. You can't vote in it."))


can_vote_poll = return_boolean(allow_vote_poll)


def allow_see_poll_votes(user_acl, target):
    if not target.is_public and not user_acl["can_always_see_poll_voters"]:
        raise PermissionDenied(_("You dont have permission to this poll's voters."))


can_see_poll_votes = return_boolean(allow_see_poll_votes)


def has_time_to_edit_poll(user_acl, target):
    edit_time = user_acl["poll_edit_time"]
    if edit_time:
        diff = timezone.now() - target.posted_on
        diff_minutes = int(diff.total_seconds() / 60)
        return diff_minutes < edit_time

    return True
