from django.utils.translation import ugettext_lazy as _

from misago.acl import algebra
from misago.acl.models import Role
from misago.core import forms


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("Deleting spammer accounts")

    can_destroy_user_newer_than = forms.IntegerField(
        label=_("Maximum age of deleted account (in days)"),
        help_text=_("Enter zero to disable this check."),
        min_value=0,
        initial=0)
    can_destroy_users_with_less_posts_than = forms.IntegerField(
        label=_("Maximum number of posts on deleted account"),
        help_text=_("Enter zero to disable this check."),
        min_value=0,
        initial=0)


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
        'can_destroy_user_newer_than': 0,
        'can_destroy_users_with_less_posts_than': 0,
    }
    new_acl.update(acl)

    return algebra.sum_acls(
            new_acl, roles=roles, key=key_name,
            can_destroy_user_newer_than=algebra.greater,
            can_destroy_users_with_less_posts_than=algebra.greater
            )
