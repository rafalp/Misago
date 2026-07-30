class ExtensionsRegistry:
    _extensions: dict[type, list[type]]

    def __init__(self):
        self._extensions = {}

    def register(self, extended_type: type, extension: type, early: bool = False):
        type_extensions = self._extensions.setdefault(extended_type, [])
        if early:
            type_extensions.insert(0, extension)
        else:
            type_extensions.append(extension)

    def get(self, extended_type: type) -> type:
        if extended_type not in self._extensions:
            return extended_type

        return type(
            f"Extended{extended_type.__name__}",
            (*reversed(self._extensions[extended_type]), extended_type),
            {},
        )


extensions = ExtensionsRegistry()


def extend(extended_type: type, early: bool = False):
    def decorator(extension: type):
        extensions.register(extended_type, extension, early)
        return extension

    return decorator
