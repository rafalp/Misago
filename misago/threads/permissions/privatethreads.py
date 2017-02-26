from django import forms
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from misago.acl import algebra
from misago.acl.decorators import return_boolean
from misago.acl.models import Role
from misago.categories import PRIVATE_THREADS_ROOT_NAME
from misago.categories.models import Category
from misago.core.forms import YesNoSwitch
from misago.threads.models import Thread


__all__ = [
    'allow_use_private_threads',
    'can_use_private_threads',
    'allow_see_private_thread',
    'can_see_private_thread',
    'allow_change_owner',
    'can_change_owner',
    'allow_add_participants',
    'can_add_participants',
    'allow_remove_participant',
    'can_remove_participant',
    'allow_add_participant',
    'can_add_participant',
    'allow_message_user',
    'can_message_user',
]


class PermissionsForm(forms.Form):
    legend = _("Private threads")

    can_use_private_threads = YesNoSwitch(label=_("Can use private threads"))
    can_start_private_threads = YesNoSwitch(label=_("Can start private threads"))
    max_private_thread_participants = forms.IntegerField(
        label=_("Max number of users invited to private thread"),
        help_text=_("Enter 0 to don't limit number of participants."),
        initial=3,
        min_value=0,
    )
    can_add_everyone_to_private_threads = YesNoSwitch(
        label=_("Can add everyone to threads"),
        help_text=_("Allows user to add users that are blocking him to private threads."),
    )
    can_report_private_threads = YesNoSwitch(
        label=_("Can report private threads"),
        help_text=_(
            "Allows user to report private threads they are "
            "participating in, making them accessible to moderators."
        ),
    )
    can_moderate_private_threads = YesNoSwitch(
        label=_("Can moderate private threads"),
        help_text=_(
            "Allows user to read, reply, edit and delete content "
            "in reported private threads."
        ),
    )


def change_permissions_form(role):
    if isinstance(role, Role) and role.special_role != 'anonymous':
        return PermissionsForm
    else:
        return None


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

    algebra.sum_acls(
        new_acl,
        roles=roles,
        key=key_name,
        can_use_private_threads=algebra.greater,
        can_start_private_threads=algebra.greater,
        max_private_thread_participants=algebra.greater_or_zero,
        can_add_everyone_to_private_threads=algebra.greater,
        can_report_private_threads=algebra.greater,
        can_moderate_private_threads=algebra.greater
    )

    if not new_acl['can_use_private_threads']:
        return new_acl

    private_category = Category.objects.private_threads()

    new_acl['visible_categories'].append(private_category.pk)
    new_acl['browseable_categories'].append(private_category.pk)

    if new_acl['can_moderate_private_threads']:
        new_acl['can_see_reports'].append(private_category.pk)

    category_acl = {
        'can_see': 1,
        'can_browse': 1,
        'can_see_all_threads': 1,
        'can_see_own_threads': 0,
        'can_start_threads': new_acl['can_start_private_threads'],
        'can_reply_threads': 1,
        'can_edit_threads': 1,
        'can_edit_posts': 1,
        'can_hide_own_threads': 0,
        'can_hide_own_posts': 1,
        'thread_edit_time': 0,
        'post_edit_time': 0,
        'can_hide_threads': 0,
        'can_hide_posts': 0,
        'can_protect_posts': 0,
        'can_move_posts': 0,
        'can_merge_posts': 0,
        'can_pin_threads': 0,
        'can_close_threads': 0,
        'can_move_threads': 0,
        'can_merge_threads': 0,
        'can_approve_content': 0,
        'can_report_content': new_acl['can_report_private_threads'],
        'can_see_reports': 0,
        'can_see_posts_likes': 0,
        'can_like_posts': 0,
        'can_hide_events': 0,
    }

    if new_acl['can_moderate_private_threads']:
        category_acl.update({
            'can_edit_threads': 2,
            'can_edit_posts': 2,
            'can_hide_threads': 2,
            'can_hide_posts': 2,
            'can_protect_posts': 1,
            'can_merge_posts': 1,
            'can_see_reports': 1,
            'can_close_threads': 1,
            'can_hide_events': 2,
        })

    new_acl['categories'][private_category.pk] = category_acl

    return new_acl


def add_acl_to_thread(user, thread):
    if thread.thread_type.root_name != PRIVATE_THREADS_ROOT_NAME:
        return

    if not hasattr(thread, 'participant'):
        thread.participants_list = []
        thread.participant = None

    thread.acl.update({
        'can_start_poll': False,
        'can_change_owner': can_change_owner(user, thread),
        'can_add_participants': can_add_participants(user, thread),
    })


def register_with(registry):
    registry.acl_annotator(Thread, add_acl_to_thread)


def allow_use_private_threads(user):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to use private threads."))
    if not user.acl_cache['can_use_private_threads']:
        raise PermissionDenied(_("You can't use private threads."))


can_use_private_threads = return_boolean(allow_use_private_threads)


def allow_see_private_thread(user, target):
    if user.acl_cache['can_moderate_private_threads']:
        can_see_reported = target.has_reported_posts
    else:
        can_see_reported = False

    can_see_participating = user in [p.user for p in target.participants_list]

    if not (can_see_participating or can_see_reported):
        raise Http404()


can_see_private_thread = return_boolean(allow_see_private_thread)


def allow_change_owner(user, target):
    is_moderator = user.acl_cache['can_moderate_private_threads']
    is_owner = target.participant and target.participant.is_owner

    if not (is_owner or is_moderator):
        raise PermissionDenied(_("Only thread owner and moderators can change threads owners."))

    if not is_moderator and target.is_closed:
        raise PermissionDenied(_("Only moderators can change closed threads owners."))


can_change_owner = return_boolean(allow_change_owner)


def allow_add_participants(user, target):
    is_moderator = user.acl_cache['can_moderate_private_threads']

    if not is_moderator:
        if not target.participant or not target.participant.is_owner:
            raise PermissionDenied(_("You have to be thread owner to add new participants to it."))

        if target.is_closed:
            raise PermissionDenied(_("Only moderators can add participants to closed threads."))

    max_participants = user.acl_cache['max_private_thread_participants']
    current_participants = len(target.participants_list) - 1

    if current_participants >= max_participants:
        raise PermissionDenied(_("You can't add any more new users to this thread."))


can_add_participants = return_boolean(allow_add_participants)


def allow_remove_participant(user, thread, target):
    if user.acl_cache['can_moderate_private_threads']:
        return

    if user == target:
        return  # we can always remove ourselves

    if thread.is_closed:
        raise PermissionDenied(_("Only moderators can remove participants from closed threads."))

    if not thread.participant or not thread.participant.is_owner:
        raise PermissionDenied(_("You have to be thread owner to remove participants from it."))


can_remove_participant = return_boolean(allow_remove_participant)


def allow_add_participant(user, target):
    message_format = {'user': target.username}

    if not can_use_private_threads(target):
        raise PermissionDenied(
            _("%(user)s can't participate in private threads.") % message_format
        )

    if user.acl_cache['can_add_everyone_to_private_threads']:
        return

    if user.acl_cache['can_be_blocked'] and target.is_blocking(user):
        raise PermissionDenied(_("%(user)s is blocking you.") % message_format)

    if target.can_be_messaged_by_nobody:
        raise PermissionDenied(
            _("%(user)s is not allowing invitations to private threads.") % message_format
        )

    if target.can_be_messaged_by_followed and not target.is_following(user):
        message = _("%(user)s limits invitations to private threads to followed users.")
        raise PermissionDenied(message % message_format)


can_add_participant = return_boolean(allow_add_participant)


def allow_message_user(user, target):
    allow_use_private_threads(user)
    allow_add_participant(user, target)


can_message_user = return_boolean(allow_message_user)
