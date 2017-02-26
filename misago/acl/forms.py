from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Role
from .providers import providers


class RoleForm(forms.ModelForm):
    name = forms.CharField(label=_("Role name"))

    class Meta:
        model = Role
        fields = ['name']


def get_permissions_forms(role, data=None):
    """utility function for building forms in admin"""
    role_permissions = role.permissions

    perms_forms = []
    for extension, module in providers.list():
        try:
            module.change_permissions_form
        except AttributeError:
            message = "'%s' object has no attribute '%s'"
            raise AttributeError(message % (extension, 'change_permissions_form'))

        FormType = module.change_permissions_form(role)

        if FormType:
            if data:
                perms_forms.append(FormType(
                    data,
                    prefix=extension,
                ))
            else:
                perms_forms.append(
                    FormType(
                        initial=role_permissions.get(extension),
                        prefix=extension,
                    )
                )

    return perms_forms
