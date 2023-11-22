import sys
from pathlib import Path
from typing import List


def discover_plugins(plugins_path: str | None) -> List[str]:
    if not plugins_path:
        return []

    plugins_path_obj = Path(plugins_path)
    if not plugins_path_obj.is_dir():
        print("HERE")
        return []

    return discover_plugins_in_directory(plugins_path_obj)


def discover_plugins_in_directory(plugins_path: Path) -> List[str]:
    plugins_apps: List[str] = []

    for plugin_path in plugins_path.glob("*/*/misago_plugin.py"):
        plugin_package = plugin_path.parent

        # Add plugin to Python path so its importable
        plugin_dir = str(plugin_package.parent)
        if plugin_dir not in sys.path:
            sys.path.append(plugin_dir)

        # Add plugin to apps to make Django include it
        plugins_apps.append(plugin_package.name)

    return plugins_apps
