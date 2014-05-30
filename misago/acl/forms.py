from django.utils.translation import ugettext_lazy as _
from misago.core import forms
from misago.acl.models import Role, ForumRole


class RoleForm(forms.ModelForm):
    name = forms.CharField(label=_("Role name"))

    class Meta:
        model = Role
        fields = ['name']


class ForumRoleForm(forms.ModelForm):
    name = forms.CharField(label=_("Role name"))

    class Meta:
        model = ForumRole
        fields = ['name']
