import os
import sys
from types import ModuleType
from typing import List, Optional, Tuple

from .plugin import Plugin
from .discovery import discover_plugins


class PluginLoader:
    _plugins: List[Plugin]

    def __init__(self, plugins_root_path: Optional[str]):
        if plugins_root_path:
            self._plugins = discover_plugins(plugins_root_path)
            for plugin in self._plugins:
                sys.path.append(plugin.get_path())
        else:
            self._plugins = []

    def import_modules_if_exists(
        self, module_name: str
    ) -> List[Tuple[str, ModuleType]]:
        modules = []
        for plugin in self._plugins:
            module = plugin.import_module_if_exists(module_name)
            if module:
                modules.append((plugin, module))

        return modules

    def get_plugins_with_directory(self, directory_name: str) -> List[Plugin]:
        plugins = []
        for plugin in self._plugins:
            if plugin.has_directory(directory_name):
                plugins.append(
                    (plugin, os.path.join(plugin.get_path(), directory_name))
                )
        return plugins
