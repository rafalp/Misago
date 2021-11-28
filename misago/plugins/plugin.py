import os
from importlib import import_module
from importlib.util import find_spec
from types import ModuleType
from typing import Optional


class Plugin:
    path: str
    package_name: str

    def __init__(self, path: str, package_name: str):
        self.path = path
        self.package_name = package_name

    def __repr__(self):
        return f"<Plugin:{self.package_name}>"

    def import_module_if_exists(self, module_name: str) -> Optional[ModuleType]:
        module_path = f"{self.package_name}.{module_name}"
        if find_spec(module_path):
            return import_module(module_path)

        return None

    def import_module(self, module_name: str) -> ModuleType:
        module = self.import_module_if_exists(module_name)
        if module:
            return module

        raise ImportError(
            f"Plugin {self.package_name} has no module named '{module_name}'"
        )

    def get_path(self) -> str:
        return self.path

    def has_directory(self, directory_name: str) -> bool:
        directory_path = os.path.join(self.path, directory_name)
        return os.path.isdir(directory_path)
