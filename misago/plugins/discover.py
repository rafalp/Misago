import importlib
import re
import sys
from pathlib import Path
from typing import Dict, List


def discover_plugins(plugins_path: str | None) -> List[str]:
    if not plugins_path:
        return []

    plugins_path_obj = Path(plugins_path)
    if not plugins_path_obj.is_dir():
        return []

    plugins_apps = discover_plugins_in_directory(plugins_path_obj)

    pip_install = plugins_path_obj / "pip-install.txt"
    if pip_install.is_file():
        plugins_apps += discover_plugins_in_pip_install(pip_install)

    return sorted(plugins_apps)


def discover_plugins_in_directory(plugins_path: Path) -> List[str]:
    plugins_apps: List[str] = []
    plugins_paths: Dict[str, str] = {}

    # First step: glob plugin Python packages
    for plugin_path in sorted(plugins_path.glob("*/*/misago_plugin.py")):
        plugin_package = plugin_path.parent

        # Skip plugins that are not valid Python packages
        plugin_package_init = plugin_package / "__init__.py"
        if not plugin_package_init.is_file():
            continue

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


def discover_plugins_in_pip_install(pip_install_path: Path) -> List[str]:
    pip_install_lines = read_pip_install_file(pip_install_path)
    return validate_modules_from_pip_install(pip_install_lines)


PIP_LINE_RE = re.compile(r"^[a-z0-9-_]+")


def read_pip_install_file(pip_install_path: Path) -> List[str]:
    clean_lines: List[str] = []
    with open(pip_install_path, "r") as fp:
        file_lines: List[str] = fp.readlines()
        for file_line in file_lines:
            clean_line = file_line.strip()
            if clean_line.startswith("#"):
                continue

            if "#" in clean_line:
                comment_start = clean_line.find("#")
                clean_line = clean_line[:comment_start].strip()

            clean_line_match = PIP_LINE_RE.match(clean_line)
            if not clean_line_match:
                continue

            clean_line = clean_line_match.group(0).replace("-", "_")
            if clean_line and clean_line not in clean_lines:
                clean_lines.append(clean_line)

    return clean_lines


def validate_modules_from_pip_install(pip_install_lines: List[str]) -> List[str]:
    valid_lines: List[str] = []
    for pip_install_line in pip_install_lines:
        try:
            module = importlib.import_module(pip_install_line)
            module_path = Path(module.__file__).parent
            if not module_path.is_dir():
                continue
            misago_plugin_path = module_path / "misago_plugin.py"
            if not misago_plugin_path.is_file():
                continue
            valid_lines.append(pip_install_line)
        except:
            pass
    return valid_lines
