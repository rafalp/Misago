from os import path
from pathlib import Path
from typing import List

from .plugin import Plugin


def discover_plugins(plugins_root: str) -> List[Plugin]:
    plugins = []
    for plugin_path in Path(plugins_root).glob("*/*/plugin.py"):
        plugins.append(
            Plugin(
                path.dirname(plugin_path),
                plugin_path.parts[-3],
                plugin_path.parts[-2],
            )
        )
    return plugins


def discover_admin_plugins(plugins_root: str) -> List[str]:
    plugins = []
    for plugin_path in Path(plugins_root).glob("*/admin/src"):
        plugins.append(str(plugin_path.parts[-3]))
    return plugins


def discover_client_plugins(plugins_root: str) -> List[str]:
    plugins = []
    for plugin_path in Path(plugins_root).glob("*/client/src"):
        plugins.append(str(plugin_path.parts[-3]))
    return plugins
