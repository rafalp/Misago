from importlib import import_module
from django.conf import settings


__ALL__ = ['providers']


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
