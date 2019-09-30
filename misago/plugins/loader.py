import sys
from typing import List, Optional, Tuple
from types import ModuleType

from .plugin import Plugin
from .pluginlist import load_plugin_list_if_exists


class PluginLoader:
    _plugins: List[Plugin]

    def __init__(self, plugin_list_path: Optional[str]):
        if plugin_list_path:
            self._plugins = self.load_plugins(plugin_list_path)
        else:
            self._plugins = []

    def load_plugins(self, plugin_list_path: str) -> List["Plugin"]:
        plugins = load_plugin_list_if_exists(plugin_list_path)
        if not plugins:
            return []

        loaded_plugins = []
        for plugin in plugins:
            if "@" in plugin:
                plugin, path = plugin.split("@", 1)
                sys.path.append(path)
            loaded_plugins.append(Plugin(plugin))

        return loaded_plugins

    def import_module_if_exists(self, module_name: str) -> List[Tuple[str, ModuleType]]:
        modules = []
        for plugin in self._plugins:
            module = plugin.import_module_if_exists(module_name)
            if module:
                modules.append((plugin.module_name, module))

        return modules
