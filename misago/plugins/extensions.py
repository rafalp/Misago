class ExtensionRegistry:
    _extensions: dict[type, list[type]]
    _cache: dict[type, type]

    def __init__(self):
        self._extensions = {}
        self._cache = {}

    def register(self, base_type: type, extension_type: type, prepend: bool = False):
        type_extensions = self._extensions.setdefault(base_type, [])
        if prepend:
            type_extensions.insert(0, extension_type)
        else:
            type_extensions.append(extension_type)

        self._cache.pop(base_type, None)

    def get(self, base_type: type) -> type:
        if base_type not in self._extensions:
            return base_type

        if base_type not in self._cache:
            self._cache[base_type] = self.extend_type(base_type)

        return self._cache[base_type]

    def extend_type(self, base_type: type) -> type:
        return type(
            f"Extended{base_type.__name__}",
            (*reversed(self._extensions[base_type]), base_type),
            {},
        )


extensions = ExtensionRegistry()


def extends(base_type: type, prepend: bool = False):
    def decorator(extension_type: type):
        extensions.register(base_type, extension_type, prepend)
        return extension_type

    return decorator
