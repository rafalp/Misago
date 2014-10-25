from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from misago.acl import add_acl, algebra
from misago.acl.decorators import return_boolean
from misago.core import forms
from misago.forums.models import Forum, RoleForumACL, ForumRole
from misago.forums.permissions import get_forums_roles

from misago.threads.models import Thread, Post, Event


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
    can_move_posts = forms.YesNoSwitch(
        label=_("Can move posts"))
    can_merge_posts = forms.YesNoSwitch(
        label=_("Can merge posts"))
    can_change_threads_labels = forms.TypedChoiceField(
        label=_("Can change threads labels"), coerce=int, initial=0,
        choices=((0, _("No")), (1, _("Own threads")), (2, _("All threads"))))
    can_pin_threads = forms.YesNoSwitch(
        label=_("Can pin threads"))
    can_close_threads = forms.YesNoSwitch(label=_("Can close threads"))
    can_move_threads = forms.YesNoSwitch(
        label=_("Can move threads"))
    can_merge_threads = forms.YesNoSwitch(
        label=_("Can merge threads"))
    can_split_threads = forms.YesNoSwitch(
        label=_("Can split threads"))
    can_review_moderated_content = forms.YesNoSwitch(
        label=_("Can review moderated content"),
        help_text=_("Will see and be able to accept moderated content."))
    can_report_content = forms.YesNoSwitch(label=_("Can report posts"))
    can_see_reports = forms.YesNoSwitch(label=_("Can see reports"))
    can_hide_events = forms.TypedChoiceField(
        label=_("Can hide events"),
        coerce=int,
        initial=0,
        choices=(
            (0, _("No")),
            (1, _("Hide events")),
            (2, _("Delete events"))
        ))


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
        'can_move_posts': 0,
        'can_merge_posts': 0,
        'can_change_threads_labels': 0,
        'can_pin_threads': 0,
        'can_close_threads': 0,
        'can_move_threads': 0,
        'can_merge_threads': 0,
        'can_split_threads': 0,
        'can_review_moderated_content': 0,
        'can_report_content': 0,
        'can_see_reports': 0,
        'can_hide_events': 0,
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
        can_move_posts=algebra.greater,
        can_merge_posts=algebra.greater,
        can_change_threads_labels=algebra.greater,
        can_pin_threads=algebra.greater,
        can_close_threads=algebra.greater,
        can_move_threads=algebra.greater,
        can_merge_threads=algebra.greater,
        can_split_threads=algebra.greater,
        can_review_moderated_content=algebra.greater,
        can_report_content=algebra.greater,
        can_see_reports=algebra.greater,
        can_hide_events=algebra.greater,
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
    if isinstance(target, Event):
        add_acl_to_event(user, target)


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
        'can_move_posts': 0,
        'can_merge_posts': 0,
        'can_change_threads_labels': 0,
        'can_pin_threads': 0,
        'can_close_threads': 0,
        'can_move_threads': 0,
        'can_merge_threads': 0,
        'can_split_threads': 0,
        'can_review_moderated_content': 0,
        'can_report_content': 0,
        'can_see_reports': 0,
        'can_hide_events': 0,
    })

    algebra.sum_acls(forum.acl, acls=[forum_acl],
        can_see_all_threads=algebra.greater)

    if user.is_authenticated():
        algebra.sum_acls(forum.acl, acls=[forum_acl],
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
            can_move_posts=algebra.greater,
            can_merge_posts=algebra.greater,
            can_change_threads_labels=algebra.greater,
            can_pin_threads=algebra.greater,
            can_close_threads=algebra.greater,
            can_move_threads=algebra.greater,
            can_merge_threads=algebra.greater,
            can_split_threads=algebra.greater,
            can_review_moderated_content=algebra.greater,
            can_report_content=algebra.greater,
            can_see_reports=algebra.greater,
            can_hide_events=algebra.greater,
        )

    forum.acl['can_see_own_threads'] = not forum.acl['can_see_all_threads']


def add_acl_to_thread(user, thread):
    forum_acl = user.acl['forums'].get(thread.forum_id, {})

    thread.acl.update({
        'can_reply': can_reply_thread(user, thread),
        'can_hide': forum_acl.get('can_hide_threads'),
        'can_change_label': forum_acl.get('can_change_threads_labels') == 2,
        'can_pin': forum_acl.get('can_pin_threads'),
        'can_close': forum_acl.get('can_close_threads'),
        'can_move': forum_acl.get('can_move_threads'),
        'can_review': forum_acl.get('can_review_moderated_content'),
        'can_report': forum_acl.get('can_report'),
        'can_see_reports': forum_acl.get('can_see_reports')
    })

    if can_change_owned_thread(user, thread):
        if not thread.acl['can_change_label']:
            can_change_label = forum_acl.get('can_change_threads_labels') == 1
            thread.acl['can_change_label'] = can_change_label
        if not thread.acl['can_hide']:
            thread.acl['can_hide'] = forum_acl.get('can_hide_own_threads')


def add_acl_to_post(user, post):
    pass


def add_acl_to_event(user, event):
    forum_acl = user.acl['forums'].get(event.forum_id, {})
    can_hide_events = forum_acl.get('can_hide_events', 0)

    event.acl['can_hide'] = can_hide_events > 0
    event.acl['can_delete'] = can_hide_events == 2


"""
ACL tests
"""
def allow_see_thread(user, target):
    forum_acl = user.acl['forums'].get(target.forum_id, {})
    if not forum_acl.get('can_see_all_threads'):
        if user.is_anonymous() or user.pk != target.starter_id:
            raise Http404()
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


def allow_reply_thread(user, target):
    if target.forum.is_closed:
        message = _("This forum is closed.")
        raise PermissionDenied(message)
    if user.is_anonymous():
        raise PermissionDenied(_("You have to sign in to reply threads."))

    reply_thread = user.acl['forums'].get(target.id, {'can_reply_threads': 0})
    if reply_thread == 0:
        raise PermissionDenied(_("You can't reply to threads in this forum."))
    if target.is_closed and reply_thread < 2:
        raise PermissionDenied(
            _("You can't reply to closed threads in this forum."))
can_reply_thread = return_boolean(allow_reply_thread)


def can_change_owned_thread(user, target):
    forum_acl = user.acl['forums'].get(target.forum_id, {})

    if user.is_anonymous() or user.pk != target.starter_id:
        return False

    if target.forum.is_closed or target.is_closed:
        return False

    if target.first_post.is_protected:
        return False

    if forum_acl.get('thread_edit_time'):
        diff = timezone.now() - target.started_on
        diff_minutes = int(diff.total_seconds() / 60)

        if diff_minutes > forum_acl.get('thread_edit_time'):
            return False

    return True


def allow_see_post(user, target):
    forum_acl = user.acl['forums'].get(target.forum_id, {})
    if not forum_acl.get('can_review_moderated_content'):
        if user.is_anonymous() or user.pk != target.poster_id:
            raise Http404()
can_see_post = return_boolean(allow_see_post)


"""
Queryset helpers
"""
def exclude_invisible_threads(queryset, user, forum=None):
    if forum:
        return exclude_invisible_forum_threads(queryset, user, forum)
    else:
        return exclude_all_invisible_threads(queryset, user)


def exclude_invisible_forum_threads(queryset, user, forum):
    if user.is_authenticated():
        condition_author = Q(starter_id=user.id)

        can_mod = forum.acl['can_review_moderated_content']
        can_hide = forum.acl['can_hide_threads']

        if not can_mod and not can_hide:
            condition = Q(is_moderated=False) & Q(is_hidden=False)
            queryset = queryset.filter(condition_author | condition)
        elif not can_mod:
            condition = Q(is_moderated=False)
            queryset = queryset.filter(condition_author | condition)
        elif not can_hide:
            condition = Q(is_hidden=False)
            queryset = queryset.filter(condition_author | condition)
    else:
        if not forum.acl['can_review_moderated_content']:
            queryset = queryset.filter(is_moderated=False)
        if not forum.acl['can_hide_threads']:
            queryset = queryset.filter(is_hidden=False)

    return queryset


def exclude_all_invisible_threads(queryset, user):
    forums_in = []
    conditions = None

    for forum in Forum.objects.all_forums():
        add_acl(user, forum)

        condition_forum = Q(forum=forum)
        condition_author = Q(starter_id=user.id)

        # can see all threads?
        if forum.acl['can_see_all_threads']:
            can_mod = forum.acl['can_review_moderated_content']
            can_hide = forum.acl['can_hide_threads']

            if not can_mod or not can_hide:
                if not can_mod and not can_hide:
                    condition = Q(is_moderated=False) & Q(is_hidden=False)
                elif not can_mod:
                    condition = Q(is_moderated=False)
                elif not can_hide:
                    condition = Q(is_hidden=False)
                visibility_condition = condition_author | condition
                visibility_condition = condition_forum & visibility_condition
            else:
                # user can see everything so don't bother with rest of routine
                forums_in.append(forum.pk)
                continue
        else:
            # show all threads in forum made by user
            visibility_condition = condition_forum & condition_author

        if conditions:
            conditions = conditions | visibility_condition
        else:
            conditions = visibility_condition

    if conditions and forums_in:
        return queryset.filter(Q(forum_id__in=forums_in) | conditions)
    elif conditions:
        return queryset.filter(conditions)
    elif forums_in:
        return queryset.filter(forum_id__in=forums_in)
    else:
        return Thread.objects.none()


def exclude_invisible_posts(queryset, user, forum):
    if not forum.acl['can_review_moderated_content']:
        if user.is_authenticated():
            condition_author = Q(poster=user.id)
            condition = Q(is_moderated=False)
            queryset = queryset.filter(condition_author | condition)
        elif not forum.acl['can_review_moderated_content']:
            queryset = queryset.filter(is_moderated=False)

    return queryset
