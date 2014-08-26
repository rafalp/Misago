from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import ugettext_lazy as _


from misago.acl import algebra
from misago.acl.decorators import return_boolean
from misago.core import forms
from misago.forums.models import Forum, RoleForumACL, ForumRole
from misago.forums.permissions import get_forums_roles

from misago.threads.models import Thread, Post


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("Threads")
    can_see_all_threads = forms.TypedChoiceField(
        label=_("Can see threads"),
        coerce=int,
        initial=0,
        choices=((0, _("Started threads")), (1, _("All threads"))))
    can_start_threads = forms.YesNoSwitch(label=_("Can start threads"))
    can_reply_threads = forms.TypedChoiceField(
        label=_("Can reply to threads"),
        coerce=int,
        initial=0,
        choices=((0, _("No")), (1, _("Open threads")), (2, _("All threads"))))
    can_edit_threads = forms.TypedChoiceField(
        label=_("Can edit threads"),
        coerce=int,
        initial=0,
        choices=((0, _("No")), (1, _("Own threads")), (2, _("All threads"))))
    can_hide_own_threads = forms.TypedChoiceField(
        label=_("Can hide own threads"),
        help_text=_("Only threads started within time limit and "
                    "with no replies can be hidden."),
        coerce=int,
        initial=0,
        choices=(
            (0, _("No")),
            (1, _("Hide threads")),
            (2, _("Delete threads"))
        ))
    thread_edit_time = forms.IntegerField(
        label=_("Min. time for own thread edit, in minutes"),
        help_text=_("Enter 0 to don't limit time for editing own threads."),
        initial=0,
        min_value=0)
    can_hide_threads = forms.TypedChoiceField(
        label=_("Can hide threads"),
        coerce=int,
        initial=0,
        choices=(
            (0, _("No")),
            (1, _("Hide threads")),
            (2, _("Delete threads"))
        ))
    can_edit_replies = forms.TypedChoiceField(
        label=_("Can edit replies"),
        coerce=int,
        initial=0,
        choices=((0, _("No")), (1, _("Own replies")), (2, _("All replies"))))
    can_hide_own_replies = forms.TypedChoiceField(
        label=_("Can hide own replies"),
        help_text=_("Only last replies to thread made within "
                    "edit time limit can be hidden."),
        coerce=int,
        initial=0,
        choices=(
            (0, _("No")),
            (1, _("Hide replies")),
            (2, _("Delete replies"))
        ))
    reply_edit_time = forms.IntegerField(
        label=_("Min. time for own reply edit, in minutes"),
        help_text=_("Enter 0 to don't limit time for editing own replies."),
        initial=0,
        min_value=0)
    can_hide_replies = forms.TypedChoiceField(
        label=_("Can hide replies"),
        coerce=int,
        initial=0,
        choices=(
            (0, _("No")),
            (1, _("Hide replies")),
            (2, _("Delete replies"))
        ))
    can_protect_posts = forms.YesNoSwitch(
        label=_("Can protect posts"),
        help_text=_("Only users with this permission "
                    "can edit protected posts."))
    can_change_threads_weight = forms.TypedChoiceField(
        label=_("Can change threads weight"), coerce=int, initial=0,
        choices=(
            (0, _("No")),
            (1, _("Pin threads")),
            (2, _("Make announcements")),
        ))
    can_close_threads = forms.TypedChoiceField(
        label=_("Can close threads"),
        coerce=int,
        initial=0,
        choices=((0, _("No")), (1, _("Own threads")), (2, _("All threads"))))
    can_review_moderated_content = forms.YesNoSwitch(
        label=_("Can review moderated content"),
        help_text=_("Will see and be able to accept moderated content."))


def change_permissions_form(role):
    if isinstance(role, ForumRole):
        return PermissionsForm
    else:
        return None


"""
ACL Builder
"""
def build_acl(acl, roles, key_name):
    acl['moderated_forums'] = []
    forums_roles = get_forums_roles(roles)

    for forum in Forum.objects.all_forums():
        forum_acl = acl['forums'].get(forum.pk, {'can_browse': 0})
        if forum_acl['can_browse']:
            acl['forums'][forum.pk] = build_forum_acl(
                forum_acl, forum, forums_roles, key_name)
    return acl


def build_forum_acl(acl, forum, forums_roles, key_name):
    forum_roles = forums_roles.get(forum.pk, [])

    final_acl = {
        'can_see_all_threads': 0,
        'can_start_threads': 0,
        'can_reply_threads': 0,
        'can_edit_threads': 0,
        'can_edit_replies': 0,
        'can_hide_own_threads': 0,
        'can_hide_own_replies': 0,
        'thread_edit_time': 0,
        'reply_edit_time': 0,
        'can_hide_threads': 0,
        'can_hide_replies': 0,
        'can_protect_posts': 0,
        'can_change_threads_weight': 0,
        'can_close_threads': 0,
        'can_review_moderated_content': 0,
    }
    final_acl.update(acl)

    algebra.sum_acls(final_acl, roles=forum_roles, key=key_name,
        can_see_all_threads=algebra.greater,
        can_start_threads=algebra.greater,
        can_reply_threads=algebra.greater,
        can_edit_threads=algebra.greater,
        can_edit_replies=algebra.greater,
        can_hide_threads=algebra.greater,
        can_hide_replies=algebra.greater,
        can_hide_own_threads=algebra.greater,
        can_hide_own_replies=algebra.greater,
        thread_edit_time=algebra.greater_or_zero,
        reply_edit_time=algebra.greater_or_zero,
        can_protect_posts=algebra.greater,
        can_change_threads_weight=algebra.greater,
        can_close_threads=algebra.greater,
        can_review_moderated_content=algebra.greater,
    )

    return final_acl


"""
ACL's for targets
"""
def add_acl_to_target(user, target):
    if isinstance(target, Forum):
        add_acl_to_forum(user, target)
    if isinstance(target, Thread):
        add_acl_to_thread(user, target)
    if isinstance(target, Post):
        add_acl_to_post(user, target)


def add_acl_to_forum(user, forum):
    forum_acl = user.acl['forums'].get(forum.pk, {})

    forum.acl.update({
        'can_see_all_threads': 0,
        'can_start_threads': 0,
        'can_reply_threads': 0,
        'can_edit_threads': 0,
        'can_edit_replies': 0,
        'can_hide_own_threads': 0,
        'can_hide_own_replies': 0,
        'thread_edit_time': 0,
        'reply_edit_time': 0,
        'can_hide_threads': 0,
        'can_hide_replies': 0,
        'can_protect_posts': 0,
        'can_change_threads_weight': 0,
        'can_close_threads': 0,
        'can_review_moderated_content': 0,
    })

    if user.is_authenticated():
        algebra.sum_acls(forum.acl, acls=[forum_acl],
            can_see_all_threads=algebra.greater,
            can_start_threads=algebra.greater,
            can_reply_threads=algebra.greater,
            can_edit_threads=algebra.greater,
            can_edit_replies=algebra.greater,
            can_hide_threads=algebra.greater,
            can_hide_replies=algebra.greater,
            can_hide_own_threads=algebra.greater,
            can_hide_own_replies=algebra.greater,
            thread_edit_time=algebra.greater_or_zero,
            reply_edit_time=algebra.greater_or_zero,
            can_protect_posts=algebra.greater,
            can_change_threads_weight=algebra.greater,
            can_close_threads=algebra.greater,
            can_review_moderated_content=algebra.greater,
        )

    forum.acl['can_see_own_threads'] = not forum.acl['can_see_all_threads']


def add_acl_to_thread(user, thread):
    pass


def add_acl_to_post(user, post):
    pass


"""
ACL tests
"""
def allow_see_thread(user, target):
    forum_acl = user.acl['forums'].get(target.forum_id, {})
    if not forum_acl.get('can_see_all_threads'):
        if user.is_anonymous() or user.pk != target.starter_id:
            message = _("You can't see other users threads in this forum.")
            raise PermissionDenied(user)
can_see_thread = return_boolean(allow_see_thread)


def allow_start_thread(user, target):
    if target.is_closed:
        message = _("This forum is closed. You can't start new threads in it.")
        raise PermissionDenied(message)
    if user.is_anonymous():
        raise PermissionDenied(_("You have to sign in to start new thread."))
    if not user.acl['forums'].get(target.id, {'can_start_threads': False}):
        raise PermissionDenied(_("You don't have permission to start "
                                 "new threads in this forum."))
can_start_thread = return_boolean(allow_start_thread)
