from django.utils.translation import ugettext_lazy as _
from misago.core import forms
from misago.acl.models import Role
from misago.acl.providers import providers


class RoleForm(forms.ModelForm):
    name = forms.CharField(label=_("Role name"))

    class Meta:
        model = Role
        fields = ['name']


def get_permissions_forms(role, data=None):
    """
    Utility function for building forms in admin
    """
    role_permissions = role.permissions

    forms = []
    for provider, module in providers.list():
        try:
            default_data = module.DEFAULT_PERMISSIONS
        except AttributeError:
            message = "'%s' object has no attribute '%s'"
            raise AttributeError(
                message % (provider, 'DEFAULT_PERMISSIONS'))
        try:
            module.change_permissions_form
        except AttributeError:
            message = "'%s' object has no attribute '%s'"
            raise AttributeError(
                message % (provider, 'change_permissions_form'))

        FormType = module.change_permissions_form(role)

        if FormType:
            if data:
                forms.append(FormType(data, prefix=provider))
            else:
                initial_data = role_permissions.get(provider, default_data)
                forms.append(FormType(initial=initial_data,
                                      prefix=provider))

    return forms
