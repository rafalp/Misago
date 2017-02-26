from importlib import import_module

from django.core.exceptions import PermissionDenied

from misago.conf import settings


class SearchProviders(object):
    def __init__(self, search_providers):
        self._initialized = False
        self._providers = []

        self.providers = search_providers

    def initialize_providers(self):
        if self._initialized:
            return
        self._initialized = True

        for modulename in self.providers:
            classname = modulename.split('.')[-1]
            module_path = '.'.join(modulename.split('.')[:-1])

            try:
                module = import_module(module_path)
            except ImportError:
                raise ImportError('search module %s could not be imported' % modulename)

            try:
                classdef = getattr(module, classname)
                self._providers.append(classdef)
            except AttributeError:
                raise ImportError('search module %s could not be imported' % modulename)

    def get_providers(self, request):
        if not self._initialized:
            self.initialize_providers()

        providers = []
        for provider in self._providers:
            providers.append(provider(request))
        return providers

    def get_allowed_providers(self, request):
        allowed_providers = []
        for provider in self.get_providers(request):
            try:
                provider.allow_search()
                allowed_providers.append(provider)
            except PermissionDenied:
                pass
        return allowed_providers


searchproviders = SearchProviders(settings.MISAGO_SEARCH_EXTENSIONS)
