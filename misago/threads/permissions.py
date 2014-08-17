from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import ugettext_lazy as _


from misago.acl import algebra
from misago.acl.decorators import return_boolean
from misago.core import forms
from misago.forums.models import Forum, RoleForumACL, ForumRole

from misago.threads.models import Thread, Post


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("Forum access")
    can_see = forms.YesNoSwitch(label=_("Can see forum"))
    can_browse = forms.YesNoSwitch(label=_("Can see forum contents"))


def change_permissions_form(role):
    if isinstance(role, ForumRole):
        return PermissionsForm
    else:
        return None


"""
ACL Builder
"""
def build_acl(acl, roles, key_name):
    new_acl = {
        'visible_forums': [],
        'forums': {},
    }
    new_acl.update(acl)

    forums_roles = get_forums_roles(roles)

    for forum in Forum.objects.all_forums():
        build_forum_acl(new_acl, forum, forums_roles, key_name)

    return new_acl


def get_forums_roles(roles):
    queryset = RoleForumACL.objects.filter(role__in=roles)
    queryset = queryset.select_related('forum_role')

    forums_roles = {}
    for acl_relation in queryset.iterator():
        forum_role = acl_relation.forum_role
        forums_roles.setdefault(acl_relation.forum_id, []).append(forum_role)
    return forums_roles


def build_forum_acl(acl, forum, forums_roles, key_name):
    if forum.level > 1:
        if forum.parent_id not in acl['visible_forums']:
            # dont bother with child forums of invisible parents
            return
        elif not acl['forums'][forum.parent_id]['can_browse']:
            # parent's visible, but its contents aint
            return

    forum_roles = forums_roles.get(forum.pk, [])

    final_acl = {
        'can_see': 0,
        'can_browse': 0,
    }

    algebra.sum_acls(final_acl, roles=forum_roles, key=key_name,
        can_see=algebra.greater,
        can_browse=algebra.greater
    )

    if final_acl['can_see']:
        acl['visible_forums'].append(forum.pk)
        acl['forums'][forum.pk] = final_acl


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
    target.acl['can_see'] = can_see_forum(user, target)
    target.acl['can_browse'] = can_browse_forum(user, target)


def add_acl_to_thread(user, thread):
    pass


def add_acl_to_post(user, post):
    pass


"""
ACL tests
"""
def allow_see_forum(user, target):
    try:
        forum_id = target.pk
    except AttributeError:
        forum_id = int(target)

    if not forum_id in user.acl['visible_forums']:
        raise Http404()
can_see_forum = return_boolean(allow_see_forum)
