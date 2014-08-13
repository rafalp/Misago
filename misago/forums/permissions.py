from django.utils.translation import ugettext_lazy as _


from misago.acl import algebra
from misago.core import forms

from misago.forums.models import Forum, RoleForumACL, ForumRole


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

    algebra.sum_acls(
        final_acl, roles=forum_roles, key=key_name,
        can_see=algebra.greater,
        can_browse=algebra.greater)

    if final_acl['can_see']:
        acl['visible_forums'].append(forum.pk)
        acl['forums'][forum.pk] = final_acl


"""
ACL's for targets
"""


"""
ACL's for tests
"""
