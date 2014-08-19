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
    can_edit_replies = forms.TypedChoiceField(
        label=_("Can edit replies"),
        coerce=int,
        initial=0,
        choices=((0, _("No")), (1, _("Own replies")), (2, _("All replies"))))


def change_permissions_form(role):
    if isinstance(role, ForumRole):
        return PermissionsForm
    else:
        return None


"""
ACL Builder
"""
def build_acl(acl, roles, key_name):
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
    }
    final_acl.update(acl)

    algebra.sum_acls(final_acl, roles=forum_roles, key=key_name,
        can_see_all_threads=algebra.greater,
        can_start_threads=algebra.greater
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

    forum.acl['can_see_all_threads'] = forum_acl.get('can_see_all_threads', 0)

    if user.is_authenticated():
        forum.acl['can_start_threads'] = forum_acl.get('can_start_threads', 0)
    else:
        forum.acl['can_start_threads'] = 0


def add_acl_to_thread(user, thread):
    pass


def add_acl_to_post(user, post):
    pass


"""
ACL tests
"""
def allow_see_thread(user, target):
    raise NotImplementedError()
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
