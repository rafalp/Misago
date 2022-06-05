import os
from importlib import import_module
from importlib.util import find_spec
from types import ModuleType
from typing import Optional

from .manifest import PluginManifest


class Plugin:
    path: str
    directory_name: str
    package_name: str
    manifest: Optional[PluginManifest]

    def __init__(self, path: str, directory_name: str, package_name: str):
        self.path = path
        self.directory_name = directory_name
        self.package_name = package_name
        self.manifest = None

    def __repr__(self):
        return f"<Plugin:{self.package_name}>"

    def import_manifest(self):
        if find_spec(self.package_name):
            main_module = import_module(self.package_name)
            manifest = getattr(main_module, "__manifest__", None)
            if isinstance(manifest, PluginManifest):
                self.manifest = manifest

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
