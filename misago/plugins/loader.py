import os
import sys
from dataclasses import dataclass
from types import ModuleType
from typing import List, Optional, Tuple

from asgiref.sync import sync_to_async

from .discover import discover_admin_plugins, discover_client_plugins, discover_plugins
from .plugin import Plugin


class PluginsLoader:
    _plugins: List[Plugin]
    _admin_plugins = List[str]
    _client_plugins = List[str]

    def __init__(self, plugins_root_path: Optional[str]):
        if plugins_root_path:
            self._plugins = discover_plugins(plugins_root_path)
            for plugin in self._plugins:
                sys.path.append(os.path.dirname(plugin.get_path()))
                plugin.import_manifest()

            self._admin_plugins = discover_admin_plugins(plugins_root_path)
            self._client_plugins = discover_client_plugins(plugins_root_path)
        else:
            self._plugins = []

    def get_plugins_data(self) -> List["PluginData"]:
        done_plugins: List[str] = []
        plugins_data: List[PluginData] = []

        for plugin in self._plugins:
            done_plugins.append(plugin.directory_name)

            plugin_name = None
            plugin_description = None
            plugin_license = None
            plugin_icon = None
            plugin_color = None
            plugin_version = None
            plugin_author = None
            plugin_homepage = None
            plugin_repo = None

            if plugin.manifest:
                manifest = plugin.manifest
                plugin_name = manifest.name.strip()
                plugin_description = (manifest.description or "").strip()
                plugin_license = (manifest.license or "").strip()
                plugin_icon = (manifest.icon or "").strip()
                plugin_color = manifest.color.as_hex() if manifest.color else None
                plugin_version = (manifest.version or "").strip()
                plugin_author = (manifest.author or "").strip()
                plugin_homepage = (manifest.homepage or "").strip()
                plugin_repo = (manifest.repo or "").strip()

            plugins_data.append(
                PluginData(
                    name=plugin_name or plugin.directory_name,
                    description=plugin_description,
                    license=plugin_license or None,
                    icon=plugin_icon or None,
                    color=plugin_color or None,
                    version=plugin_version or None,
                    author=plugin_author or None,
                    homepage=plugin_homepage or None,
                    repo=plugin_repo or None,
                    directory=plugin.directory_name,
                    admin=plugin.directory_name in self._admin_plugins,
                    client=plugin.directory_name in self._client_plugins,
                )
            )

        # Get list of plugins that have js modules but miss python package
        missing_plugins = set(self._admin_plugins + self._client_plugins)
        missing_plugins -= set(done_plugins)

        for missing_plugin in missing_plugins:
            plugins_data.append(
                PluginData(
                    name=missing_plugin,
                    description=None,
                    license=None,
                    icon=None,
                    color=None,
                    version=None,
                    author=None,
                    homepage=None,
                    repo=None,
                    directory=missing_plugin,
                    admin=missing_plugin in self._admin_plugins,
                    client=missing_plugin in self._client_plugins,
                )
            )

        return sorted(plugins_data, key=lambda x: x.name)

    def import_modules_if_exists(
        self, module_name: str
    ) -> List[Tuple[Plugin, ModuleType]]:
        modules = []
        for plugin in self._plugins:
            module = plugin.import_module_if_exists(module_name)
            if module:
                modules.append((plugin, module))

        return modules

    def get_plugins_with_directory(
        self, directory_name: str
    ) -> List[Tuple[Plugin, str]]:
        plugins = []
        for plugin in self._plugins:
            if plugin.has_directory(directory_name):
                plugins.append(
                    (plugin, os.path.join(plugin.get_path(), directory_name))
                )
        return plugins


@dataclass
class PluginData:
    name: Optional[str]
    description: Optional[str]
    license: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    version: Optional[str]
    author: Optional[str]
    homepage: Optional[str]
    repo: Optional[str]
    directory: str
    admin: bool
    client: bool
