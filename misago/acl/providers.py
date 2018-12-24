from importlib import import_module

from ..conf import settings

_NOT_INITIALIZED_ERROR = (
    "PermissionProviders instance has to load providers with load() "
    "before get_obj_type_annotators(), get_user_acl_serializers(), "
    "list() or dict() methods will be available."
)

_ALREADY_INITIALIZED_ERROR = (
    "PermissionProviders instance has already loaded providers and "
    "acl_annotator or user_acl_serializer are no longer available."
)


class PermissionProviders:
    """manager for permission providers"""

    def __init__(self):
        self._initialized = False
        self._providers = []
        self._providers_dict = {}

        self._annotators = {}
        self._user_acl_serializers = []

    def load(self):
        if self._initialized:
            raise RuntimeError("providers are already loaded")

        self._register_providers()
        self._coerce_dict_values_to_tuples(self._annotators)
        self._user_acl_serializers = tuple(self._user_acl_serializers)
        self._initialized = True

    def _register_providers(self):
        for namespace in settings.MISAGO_ACL_EXTENSIONS:
            self._providers.append((namespace, import_module(namespace)))
            self._providers_dict[namespace] = import_module(namespace)

            if hasattr(self._providers_dict[namespace], "register_with"):
                self._providers_dict[namespace].register_with(self)

    def _coerce_dict_values_to_tuples(self, types_dict):
        for hashType in types_dict.keys():
            types_dict[hashType] = tuple(types_dict[hashType])

    def acl_annotator(self, hashable_type, func):
        """registers ACL annotator for specified types"""
        assert not self._initialized, _ALREADY_INITIALIZED_ERROR
        self._annotators.setdefault(hashable_type, []).append(func)

    def user_acl_serializer(self, func):
        """registers ACL serializer for specified types"""
        assert not self._initialized, _ALREADY_INITIALIZED_ERROR
        self._user_acl_serializers.append(func)

    def get_obj_type_annotators(self, obj):
        assert self._initialized, _NOT_INITIALIZED_ERROR
        return self._annotators.get(obj.__class__, [])

    def get_user_acl_serializers(self):
        assert self._initialized, _NOT_INITIALIZED_ERROR
        return self._user_acl_serializers

    def list(self):
        assert self._initialized, _NOT_INITIALIZED_ERROR
        return self._providers

    def dict(self):
        assert self._initialized, _NOT_INITIALIZED_ERROR
        return self._providers_dict


providers = PermissionProviders()
