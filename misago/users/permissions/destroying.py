from django.utils.translation import ugettext_lazy as _
from misago.acl.models import Role
from misago.core import forms


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("Destroying user accounts")
    can_destroy_user_newer_than = forms.IntegerField(
        label=_("Maximum age of destroyed account (in days)"),
        help_text=_("Enter zero to disable this check."),
        min_value=0,
        initial=0)
    can_destroy_users_with_less_posts_than = forms.IntegerField(
        label=_("Maximum number of posts on destroyed account"),
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
def build_acl(acl, roles):
    pass
