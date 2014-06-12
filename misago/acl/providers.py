from importlib import import_module
from django.conf import settings


__ALL__ = ['providers', 'get_default_permissions',
           'get_change_permissions_forms']


# Manager for permission providers
class PermissionProviders(object):
    def __init__(self):
        self._initialized = False
        self._providers = []
        self._providers_dict = {}

    def _assert_providers_imported(self):
        if not self._initialized:
            self._import_providers()
            self._initialized = True

    def _import_providers(self):
        for namespace in settings.MISAGO_PERMISSION_PROVIDERS:
            self._providers.append((namespace, import_module(namespace)))
            self._providers_dict[namespace] = import_module(namespace)

    def list(self):
        self._assert_providers_imported()
        return self._providers

    def dict(self):
        self._assert_providers_imported()
        return self._providers_dict


providers = PermissionProviders()


def get_default_permissions():
    default_permissions = {}

    for provider, module in providers.list():
        try:
            default_data = module.DEFAULT_PERMISSIONS
        except AttributeError:
            message = "'%s' object has no attribute '%s'"
            raise AttributeError(
                message % (provider, 'DEFAULT_PERMISSIONS'))

        default_permissions[provider] = default_data

    return default_permissions


def get_change_permissions_forms(role, data=None):
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
