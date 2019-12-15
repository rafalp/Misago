import os
from importlib import import_module
from importlib.util import find_spec
from types import ModuleType
from typing import Optional


class Plugin:
    module_name: str

    _module: ModuleType

    def __init__(self, module_name: str):
        self.module_name = module_name
        self._module = import_module(module_name)

    def get_main_module(self) -> ModuleType:
        return self._module

    def import_module_if_exists(self, module_name: str) -> Optional[ModuleType]:
        full_module_name = f"{self.module_name}.{module_name}"
        try:
            if find_spec(full_module_name):
                return import_module(full_module_name)
        except ModuleNotFoundError:
            pass

        return None

    def import_module(self, module_name: str) -> ModuleType:
        module = self.import_module_if_exists(module_name)
        if module:
            return module

        raise ImportError(
            f"Plugin {self.module_name} has no module named '{module_name}'"
        )

    def get_path(self) -> str:
        return os.path.abspath(os.path.dirname(self._module.__file__))

    def has_directory(self, directory_name: str) -> bool:
        plugin_path = self.get_path()
        directory_path = os.path.join(plugin_path, directory_name)
        return os.path.isdir(directory_path)
