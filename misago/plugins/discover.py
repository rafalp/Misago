import sys
from pathlib import Path
from typing import Dict, List


def discover_plugins(plugins_path: str | None) -> List[str]:
    if not plugins_path:
        return []

    plugins_path_obj = Path(plugins_path)
    if not plugins_path_obj.is_dir():
        return []

    return discover_plugins_in_directory(plugins_path_obj)


def discover_plugins_in_directory(plugins_path: Path) -> List[str]:
    plugins_apps: List[str] = []
    plugins_paths: Dict[str, str] = {}

    # First step: glob plugin Python packages
    for plugin_path in sorted(plugins_path.glob("*/*/misago_plugin.py")):
        plugin_package = plugin_path.parent

        # Add plugin package name to Django apps for later import
        plugins_apps.append(plugin_package.name)

        # Store plugin path for later adding to sys.path
        plugins_paths[plugin_package.name] = str(plugin_package.parent)

    plugins_apps = sorted(plugins_apps)

    # Add unique plugins paths to Python path ordered by app name
    for plugin_app in plugins_apps:
        plugin_path = plugins_paths[plugin_app]
        if plugin_path not in sys.path:
            sys.path.append(plugin_path)

    return plugins_apps
