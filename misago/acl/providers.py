from importlib import import_module

from misago.conf import settings


class PermissionProviders(object):
    """manager for permission providers"""

    def __init__(self):
        self._initialized = False
        self._providers = []
        self._providers_dict = {}

        self._annotators = {}
        self._serializers = {}

    def _assert_providers_registered(self):
        if not self._initialized:
            self._register_providers()
            self._change_lists_to_tupes(self._annotators)
            self._change_lists_to_tupes(self._serializers)
            self._initialized = True

    def _register_providers(self):
        for namespace in settings.MISAGO_ACL_EXTENSIONS:
            self._providers.append((namespace, import_module(namespace)))
            self._providers_dict[namespace] = import_module(namespace)

            if hasattr(self._providers_dict[namespace], 'register_with'):
                self._providers_dict[namespace].register_with(self)

    def _change_lists_to_tupes(self, types_dict):
        for hashType in types_dict.keys():
            types_dict[hashType] = tuple(types_dict[hashType])

    def acl_annotator(self, hashable_type, func):
        """registers ACL annotator for specified types"""
        self._annotators.setdefault(hashable_type, []).append(func)

    def acl_serializer(self, hashable_type, func):
        """registers ACL serializer for specified types"""
        self._serializers.setdefault(hashable_type, []).append(func)

    def get_type_annotators(self, obj):
        self._assert_providers_registered()
        return self._annotators.get(obj.__class__, [])

    def get_type_serializers(self, obj):
        self._assert_providers_registered()
        return self._serializers.get(obj.__class__, [])

    def list(self):
        self._assert_providers_registered()
        return self._providers

    def dict(self):
        self._assert_providers_registered()
        return self._providers_dict


providers = PermissionProviders()
