class ExtensionRegistry:
    _extensions: dict[type, list[type]]

    def __init__(self):
        self._extensions = {}

    def register(self, base_type: type, extension_type: type, early: bool = False):
        type_extensions = self._extensions.setdefault(base_type, [])
        if early:
            type_extensions.insert(0, extension_type)
        else:
            type_extensions.append(extension_type)

    def get(self, base_type: type) -> type:
        if base_type not in self._extensions:
            return base_type

        return type(
            f"Extended{base_type.__name__}",
            (*reversed(self._extensions[base_type]), base_type),
            {},
        )


extensions = ExtensionRegistry()


def extends(base_type: type, early: bool = False):
    def decorator(extension_type: type):
        extensions.register(base_type, extension_type, early)
        return extension_type

    return decorator
