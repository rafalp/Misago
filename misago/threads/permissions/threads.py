from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.utils.translation import ungettext, ugettext_lazy as _

from misago.acl import add_acl, algebra
from misago.acl.decorators import return_boolean
from misago.core import forms
from misago.forums.models import Forum, RoleForumACL, ForumRole
from misago.forums.permissions import get_forums_roles

from misago.threads.models import Thread, Post, Event


__all__ = [
    'register_with',
    'allow_see_thread',
    'can_see_thread',
    'allow_start_thread',
    'can_start_thread',
    'allow_reply_thread',
    'can_reply_thread',
    'allow_edit_thread',
    'can_edit_thread',
    'allow_see_post',
    'can_see_post',
    'allow_edit_post',
    'can_edit_post',
    'allow_unhide_post',
    'can_unhide_post',
    'allow_hide_post',
    'can_hide_post',
    'allow_delete_post',
    'can_delete_post',
    'exclude_invisible_threads',
    'exclude_invisible_posts'
]


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
    can_reply_threads = forms.YesNoSwitch(label=_("Can reply to threads"))
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
        label=_("Time limit for own threads edits, in minutes"),
        help_text=_("Enter 0 to don't limit time for editing own threads."),
        initial=0,
        min_value=0)
    can_hide_threads = forms.TypedChoiceField(
        label=_("Can hide all threads"),
        coerce=int,
        initial=0,
        choices=(
            (0, _("No")),
            (1, _("Hide threads")),
            (2, _("Delete threads"))
        ))
    can_edit_posts = forms.TypedChoiceField(
        label=_("Can edit posts"),
        coerce=int,
        initial=0,
        choices=((0, _("No")), (1, _("Own posts")), (2, _("All posts"))))
    can_hide_own_posts = forms.TypedChoiceField(
        label=_("Can hide own posts"),
        help_text=_("Only last posts to thread made within "
                    "edit time limit can be hidden."),
        coerce=int,
        initial=0,
        choices=(
            (0, _("No")),
            (1, _("Hide posts")),
            (2, _("Delete posts"))
        ))
    post_edit_time = forms.IntegerField(
        label=_("Time limit for own post edits, in minutes"),
        help_text=_("Enter 0 to don't limit time for editing own posts."),
        initial=0,
        min_value=0)
    can_hide_posts = forms.TypedChoiceField(
        label=_("Can hide all posts"),
        coerce=int,
        initial=0,
        choices=(
            (0, _("No")),
            (1, _("Hide posts")),
            (2, _("Delete posts"))
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
    acl['can_review_moderated_content'] = []
    acl['can_see_reports'] = []
    forums_roles = get_forums_roles(roles)

    for forum in Forum.objects.all_forums():
        forum_acl = acl['forums'].get(forum.pk, {'can_browse': 0})
        if forum_acl['can_browse']:
            acl['forums'][forum.pk] = build_forum_acl(
                forum_acl, forum, forums_roles, key_name)
            if acl['forums'][forum.pk]['can_review_moderated_content']:
                acl['can_review_moderated_content'].append(forum.pk)
            if acl['forums'][forum.pk]['can_see_reports']:
                acl['can_see_reports'].append(forum.pk)
    return acl


def build_forum_acl(acl, forum, forums_roles, key_name):
    forum_roles = forums_roles.get(forum.pk, [])

    final_acl = {
        'can_see_all_threads': 0,
        'can_start_threads': 0,
        'can_reply_threads': 0,
        'can_edit_threads': 0,
        'can_edit_posts': 0,
        'can_hide_own_threads': 0,
        'can_hide_own_posts': 0,
        'thread_edit_time': 0,
        'post_edit_time': 0,
        'can_hide_threads': 0,
        'can_hide_posts': 0,
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
        can_edit_posts=algebra.greater,
        can_hide_threads=algebra.greater,
        can_hide_posts=algebra.greater,
        can_hide_own_threads=algebra.greater,
        can_hide_own_posts=algebra.greater,
        thread_edit_time=algebra.greater_or_zero,
        post_edit_time=algebra.greater_or_zero,
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
def add_acl_to_forum(user, forum):
    forum_acl = user.acl['forums'].get(forum.pk, {})

    forum.acl.update({
        'can_see_all_threads': 0,
        'can_start_threads': 0,
        'can_reply_threads': 0,
        'can_edit_threads': 0,
        'can_edit_posts': 0,
        'can_hide_own_threads': 0,
        'can_hide_own_posts': 0,
        'thread_edit_time': 0,
        'post_edit_time': 0,
        'can_hide_threads': 0,
        'can_hide_posts': 0,
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
            can_edit_posts=algebra.greater,
            can_hide_threads=algebra.greater,
            can_hide_posts=algebra.greater,
            can_hide_own_threads=algebra.greater,
            can_hide_own_posts=algebra.greater,
            thread_edit_time=algebra.greater_or_zero,
            post_edit_time=algebra.greater_or_zero,
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
        'can_edit': can_edit_thread(user, thread),
        'can_hide': forum_acl.get('can_hide_threads'),
        'can_change_label': forum_acl.get('can_change_threads_labels') == 2,
        'can_pin': forum_acl.get('can_pin_threads'),
        'can_close': forum_acl.get('can_close_threads'),
        'can_move': forum_acl.get('can_move_threads'),
        'can_review': forum_acl.get('can_review_moderated_content'),
        'can_report': forum_acl.get('can_report_content'),
        'can_see_reports': forum_acl.get('can_see_reports')
    })

    if can_change_owned_thread(user, thread):
        if not forum_acl.get('can_close_threads'):
            thread_is_protected = thread.is_closed or thread.forum.is_closed
        else:
            thread_is_protected = False

        if not thread_is_protected:
            if not thread.acl['can_change_label']:
                can_change_label = forum_acl.get('can_change_threads_labels')
                thread.acl['can_change_label'] = can_change_label == 1
            if not thread.acl['can_hide']:
                if not thread.replies:
                    can_hide_thread = forum_acl.get('can_hide_own_threads')
                    thread.acl['can_hide'] = can_hide_thread


def add_acl_to_post(user, post):
    forum_acl = user.acl['forums'].get(post.forum_id, {})

    post.acl.update({
        'can_reply': can_reply_thread(user, post.thread),
        'can_edit': can_edit_post(user, post),
        'can_see_hidden': forum_acl.get('can_hide_posts'),
        'can_unhide': can_unhide_post(user, post),
        'can_hide': can_hide_post(user, post),
        'can_delete': can_delete_post(user, post),
        'can_protect': forum_acl.get('can_protect_posts'),
        'can_report': forum_acl.get('can_report_content'),
        'can_see_reports': forum_acl.get('can_see_reports'),
        'can_approve': forum_acl.get('can_review_moderated_content'),
    })

    if not post.is_moderated:
        post.acl['can_approve'] = False

    if not post.acl['can_see_hidden']:
        if user.is_authenticated() and user.id == post.poster_id:
            post.acl['can_see_hidden'] = True
        else:
            post.acl['can_see_hidden'] = post.id == post.thread.first_post_id


def add_acl_to_event(user, event):
    forum_acl = user.acl['forums'].get(event.forum_id, {})
    can_hide_events = forum_acl.get('can_hide_events', 0)

    event.acl['can_hide'] = can_hide_events > 0
    event.acl['can_delete'] = can_hide_events == 2


def register_with(registry):
    registry.acl_annotator(Forum, add_acl_to_forum)
    registry.acl_annotator(Thread, add_acl_to_thread)
    registry.acl_annotator(Post, add_acl_to_post)
    registry.acl_annotator(Event, add_acl_to_event)


"""
ACL tests
"""
def allow_see_thread(user, target):
    forum_acl = user.acl['forums'].get(target.forum_id, {})
    if not forum_acl.get('can_browse'):
        raise Http404()

    if user.is_anonymous() or user.pk != target.starter_id:
        if not forum_acl.get('can_see_all_threads'):
            raise Http404()
        if target.is_moderated:
            if not forum_acl.get('can_review_moderated_content'):
                raise Http404()
        if target.is_hidden and not forum_acl.get('can_hide_threads'):
            raise Http404()
can_see_thread = return_boolean(allow_see_thread)


def allow_start_thread(user, target):
    if user.is_anonymous():
        raise PermissionDenied(_("You have to sign in to start threads."))

    if target.is_closed and not target.acl['can_close_threads']:
        raise PermissionDenied(
            _("This forum is closed. You can't start new threads in it."))

    if not user.acl['forums'].get(target.id, {'can_start_threads': False}):
        raise PermissionDenied(_("You don't have permission to start "
                                 "new threads in this forum."))
can_start_thread = return_boolean(allow_start_thread)


def allow_reply_thread(user, target):
    if user.is_anonymous():
        raise PermissionDenied(_("You have to sign in to reply threads."))

    forum_acl = target.forum.acl

    if not forum_acl['can_close_threads']:
        if target.forum.is_closed:
            raise PermissionDenied(
                _("This forum is closed. You can't reply to threads in it."))
        if target.is_closed:
            raise PermissionDenied(
                _("You can't reply to closed threads in this forum."))

    if not forum_acl['can_reply_threads']:
        raise PermissionDenied(_("You can't reply to threads in this forum."))
can_reply_thread = return_boolean(allow_reply_thread)


def allow_edit_thread(user, target):
    if user.is_anonymous():
        raise PermissionDenied(_("You have to sign in to edit threads."))

    forum_acl = target.forum.acl

    if not forum_acl['can_edit_threads']:
        raise PermissionDenied(_("You can't edit threads in this forum."))

    if forum_acl['can_edit_threads'] == 1:
        if target.starter_id != user.pk:
            raise PermissionDenied(
                _("You can't edit other users threads in this forum."))

        if not forum_acl['can_close_threads']:
            if target.forum.is_closed:
                raise PermissionDenied(
                    _("This forum is closed. You can't edit threads in it."))
            if target.is_closed:
                raise PermissionDenied(
                    _("You can't edit closed threads in this forum."))

        if not has_time_to_edit_thread(user, target):
            message = ungettext("You can't edit threads that are "
                                "older than %(minutes)s minute.",
                                "You can't edit threads that are "
                                "older than %(minutes)s minutes.",
                                forum_acl['thread_edit_time'])
            raise PermissionDenied(
                message % {'minutes': forum_acl['thread_edit_time']})
can_edit_thread = return_boolean(allow_edit_thread)


def allow_see_post(user, target):
    if target.is_moderated:
        forum_acl = user.acl['forums'].get(target.forum_id, {})
        if not forum_acl.get('can_review_moderated_content'):
            if user.is_anonymous() or user.pk != target.poster_id:
                raise Http404()
can_see_post = return_boolean(allow_see_post)


def allow_edit_post(user, target):
    if user.is_anonymous():
        raise PermissionDenied(_("You have to sign in to edit posts."))

    forum_acl = target.forum.acl

    if not forum_acl['can_edit_posts']:
        raise PermissionDenied(_("You can't edit posts in this forum."))

    if target.is_hidden and not can_unhide_post(user, target):
        raise PermissionDenied(_("This post is hidden, you can't edit it."))

    if forum_acl['can_edit_posts'] == 1:
        if target.poster_id != user.pk:
            raise PermissionDenied(
                _("You can't edit other users posts in this forum."))

        if not forum_acl['can_close_threads']:
            if target.forum.is_closed:
                raise PermissionDenied(
                    _("This forum is closed. You can't edit posts in it."))
            if target.thread.is_closed:
                raise PermissionDenied(
                    _("This thread is closed. You can't edit posts in it."))

        if target.is_protected and not forum_acl['can_protect_posts']:
            raise PermissionDenied(
                _("This post is protected. You can't edit it."))

        if not has_time_to_edit_post(user, target):
            message = ungettext("You can't edit posts that are "
                                "older than %(minutes)s minute.",
                                "You can't edit posts that are "
                                "older than %(minutes)s minutes.",
                                forum_acl['post_edit_time'])
            raise PermissionDenied(
                message % {'minutes': forum_acl['post_edit_time']})
can_edit_post = return_boolean(allow_edit_post)


def allow_unhide_post(user, target):
    if user.is_anonymous():
        raise PermissionDenied(_("You have to sign in to reveal posts."))

    forum_acl = target.forum.acl

    if not forum_acl['can_hide_posts']:
        if not forum_acl['can_hide_own_posts']:
            raise PermissionDenied(_("You can't reveal posts in this forum."))

        if user.id != target.poster_id:
            raise PermissionDenied(
                _("You can't reveal other users posts in this forum."))

        if not forum_acl['can_close_threads']:
            if target.forum.is_closed:
                raise PermissionDenied(_("This forum is closed. You can't "
                                         "reveal posts in it."))
            if target.thread.is_closed:
                raise PermissionDenied(_("This thread is closed. You can't "
                                         "reveal posts in it."))

        if target.is_protected and not forum_acl['can_protect_posts']:
            raise PermissionDenied(
                _("This post is protected. You can't reveal it."))

        if has_time_to_edit_post(user, target):
            message = ungettext("You can't reveal posts that are "
                                "older than %(minutes)s minute.",
                                "You can't reveal posts that are "
                                "older than %(minutes)s minutes.",
                                forum_acl['post_edit_time'])
            raise PermissionDenied(
                message % {'minutes': forum_acl['post_edit_time']})

    if target.id == target.thread.first_post_id:
        raise PermissionDenied(_("You can't reveal thread's first post."))
    if not target.is_hidden:
        raise PermissionDenied(_("Only hidden posts can be revealed."))
can_unhide_post = return_boolean(allow_unhide_post)


def allow_hide_post(user, target):
    if user.is_anonymous():
        raise PermissionDenied(_("You have to sign in to hide posts."))

    forum_acl = target.forum.acl

    if not forum_acl['can_hide_posts']:
        if not forum_acl['can_hide_own_posts']:
            raise PermissionDenied(_("You can't hide posts in this forum."))

        if user.id != target.poster_id:
            raise PermissionDenied(
                _("You can't hide other users posts in this forum."))

        if not forum_acl['can_close_threads']:
            if target.forum.is_closed:
                raise PermissionDenied(_("This forum is closed. You can't "
                                         "hide posts in it."))
            if target.thread.is_closed:
                raise PermissionDenied(_("This thread is closed. You can't "
                                         "hide posts in it."))

        if target.is_protected and not forum_acl['can_protect_posts']:
            raise PermissionDenied(
                _("This post is protected. You can't hide it."))

        if has_time_to_edit_post(user, target):
            message = ungettext("You can't hide posts that are "
                                "older than %(minutes)s minute.",
                                "You can't hide posts that are "
                                "older than %(minutes)s minutes.",
                                forum_acl['post_edit_time'])
            raise PermissionDenied(
                message % {'minutes': forum_acl['post_edit_time']})

    if target.id == target.thread.first_post_id:
        raise PermissionDenied(_("You can't hide thread's first post."))
    if target.is_hidden:
        raise PermissionDenied(_("Only visible posts can be hidden."))
can_hide_post = return_boolean(allow_hide_post)


def allow_delete_post(user, target):
    if user.is_anonymous():
        raise PermissionDenied(_("You have to sign in to delete posts."))

    forum_acl = target.forum.acl

    if forum_acl['can_hide_posts'] != 2:
        if not forum_acl['can_hide_own_posts'] != 2:
            raise PermissionDenied(_("You can't delete posts in this forum."))

        if user.id != target.poster_id:
            raise PermissionDenied(
                _("You can't delete other users posts in this forum."))

        if not forum_acl['can_close_threads']:
            if target.forum.is_closed:
                raise PermissionDenied(_("This forum is closed. You can't "
                                         "delete posts from it."))
            if target.thread.is_closed:
                raise PermissionDenied(_("This thread is closed. You can't "
                                         "delete posts from it."))

        if target.is_protected and not forum_acl['can_protect_posts']:
            raise PermissionDenied(
                _("This post is protected. You can't delete it."))

        if has_time_to_edit_post(user, target):
            message = ungettext("You can't delete posts that are "
                                "older than %(minutes)s minute.",
                                "You can't delete posts that are "
                                "older than %(minutes)s minutes.",
                                forum_acl['post_edit_time'])
            raise PermissionDenied(
                message % {'minutes': forum_acl['post_edit_time']})

    if target.id == target.thread.first_post_id:
        raise PermissionDenied(_("You can't delete thread's first post."))
can_delete_post = return_boolean(allow_delete_post)


"""
Permission check helpers
"""
def can_change_owned_thread(user, target):
    forum_acl = user.acl['forums'].get(target.forum_id, {})

    if user.is_anonymous() or user.pk != target.starter_id:
        return False

    if target.forum.is_closed or target.is_closed:
        return False

    if target.first_post.is_protected:
        return False

    return has_time_to_edit_thread(user, target)


def has_time_to_edit_thread(user, target):
    forum_acl = user.acl['forums'].get(target.forum_id, {})
    if forum_acl.get('thread_edit_time'):
        diff = timezone.now() - target.started_on
        diff_minutes = int(diff.total_seconds() / 60)

        return diff_minutes < forum_acl.get('thread_edit_time')
    else:
        return True


def has_time_to_edit_post(user, target):
    forum_acl = user.acl['forums'].get(target.forum_id, {})
    if forum_acl.get('post_edit_time'):
        diff = timezone.now() - target.posted_on
        diff_minutes = int(diff.total_seconds() / 60)

        return diff_minutes < forum_acl.get('post_edit_time')
    else:
        return True


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
            condition_author = Q(poster_id=user.id)
            condition = Q(is_moderated=False)
            queryset = queryset.filter(condition_author | condition)
        else:
            queryset = queryset.filter(is_moderated=False)

    return queryset
