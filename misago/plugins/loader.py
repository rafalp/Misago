import sys
from importlib import import_module
from typing import List, Optional, Tuple
from types import ModuleType

from .pluginlist import load_plugin_list_if_exists


class PluginLoader:
    _plugins: List["Plugin"]

    def __init__(self, plugin_list_path: Optional[str]):
        if plugin_list_path:
            self._plugins = self.load_plugins(plugin_list_path)
        else:
            self._plugins = []

    def load_plugins(self, plugin_list_path: Optional[str]) -> Optional[List["Plugin"]]:
        plugins = []
        for plugin in load_plugin_list_if_exists(plugin_list_path):
            if ":" in plugin:
                path, plugin = plugin.split(":")
                sys.path.append(path)
            plugins.append(Plugin(plugin))
        return plugins

    def import_modules_if_exists(
        self, module_name: str
    ) -> List[Tuple[str, ModuleType]]:
        modules = []
        for plugin in self._plugins:
            module = plugin.import_module_if_exists(module_name)
            if module:
                modules.append((plugin.module_name, module))

        return modules


class Plugin:
    module_name: str

    _module: ModuleType

    def __init__(self, module_name: str):
        self.module_name = module_name
        self._module = import_module(module_name)

    def import_module(self, module_name: str) -> ModuleType:
        return import_module(f"{self.module_name}.{module_name}")

    def import_module_if_exists(self, module_name: str) -> Optional[ModuleType]:
        try:
            return self.import_module(module_name)
        except ImportError:
            return None
