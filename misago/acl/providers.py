from importlib import import_module
from django.conf import settings


class PermissionProviders(object):
    def __init__(self):
        self._initialized = False
        self._providers = []
        self._providers_dict = {}

    def initialize_providers(self):
        if not self._initialized:
            self.import_providers()
            self._initialized = True

    def import_providers(self):
        for namespace in settings.MISAGO_PERMISSION_PROVIDERS:
            self._providers.append((namespace, import_module(namespace)))
            self._providers_dict[namespace] = import_module(namespace)

    def get_default_permissions(self):
        default_permissions = {}

        for provider, module in self._providers:
            try:
                default_data = module.DEFAULT_PERMISSIONS
            except AttributeError:
                message = "'%s' object has no attribute '%s'"
                raise AttributeError(
                    message % (provider, 'DEFAULT_PERMISSIONS'))

        default_permissions


    def get_change_permissions_forms(self, role, data=None):
        self.initialize_providers()
        role_permissions = role.permissions

        forms = []
        for provider, module in self._providers:
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

    def build_acl_cache(self, roles):
        self.initialize_providers()

    def hydrate_acl_cache(self, acl):
        self.initialize_providers()

    def get_acl_by_token(self, token):
        pass

    def get_acl_by_roles(self, roles):
        pass


providers = PermissionProviders()
