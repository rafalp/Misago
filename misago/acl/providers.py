from importlib import import_module

from misago.conf import settings


_NOT_INITIALIZED_ERROR = (
    "PermissionProviders instance has to load providers with load() "
    "before get_obj_type_annotators(), get_obj_type_serializers(), "
    "list() or dict() methods will be available."
)

_ALREADY_INITIALIZED_ERROR = (
    "PermissionProviders instance has already loaded providers and "
    "acl_annotator or acl_serializer are no longer available."
)


class PermissionProviders(object):
    """manager for permission providers"""

    def __init__(self):
        self._initialized = False
        self._providers = []
        self._providers_dict = {}

        self._annotators = {}
        self._serializers = {}

    def load(self):
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
        assert not self._initialized, _ALREADY_INITIALIZED_ERROR
        self._annotators.setdefault(hashable_type, []).append(func)

    def acl_serializer(self, hashable_type, func):
        """registers ACL serializer for specified types"""
        assert not self._initialized, _ALREADY_INITIALIZED_ERROR
        self._serializers.setdefault(hashable_type, []).append(func)

    def get_obj_type_annotators(self, obj):
        assert self._initialized, _NOT_INITIALIZED_ERROR
        return self._annotators.get(obj.__class__, [])

    def get_obj_type_serializers(self, obj):
        assert self._initialized, _NOT_INITIALIZED_ERROR
        return self._serializers.get(obj.__class__, [])

    def list(self):
        assert self._initialized, _NOT_INITIALIZED_ERROR
        return self._providers

    def dict(self):
        assert self._initialized, _NOT_INITIALIZED_ERROR
        return self._providers_dict


providers = PermissionProviders()
