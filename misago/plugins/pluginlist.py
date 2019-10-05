import os
import sys
from typing import Dict, List, Optional, Tuple


def load_plugin_list_if_exists(path: str) -> Optional[List[str]]:
    if not os.path.exists(path):
        return None

    plugins = []
    for plugin in load_plugin_list(path):
        if "@" in plugin:
            plugin, path = plugin.split("@", 1)
            sys.path.append(path)
        plugins.append(plugin)

    return plugins


def load_plugin_list(path: str) -> List[str]:
    with open(path, "r") as f:
        data = f.read()
        return parse_plugins_list(data)


def parse_plugins_list(data: str) -> List[str]:
    plugins: List[str] = []
    modules: Dict[str, Tuple[int, str]] = {}

    for line, entry in enumerate(data.splitlines()):
        plugin = entry.strip()

        if "#" in plugin:
            comment_start = plugin.find("#")
            plugin = plugin[:comment_start].strip()
        if not plugin:
            continue

        if "@" in plugin:
            module, path = map(lambda x: x.strip(), plugin.split("@", 1))
            plugin = f"{module}@{path}"
            validate_local_plugin(line, module, path)
        else:
            module = plugin
        if module in modules:
            first_line, first_entry = modules[module]
            raise ValueError(
                f"plugin '{module}' is listed more than once: "
                f"at line {first_line} ('{first_entry}') and at {line} ('{entry}')"
            )
        modules[module] = line, entry

        plugins.append(plugin)

    return plugins


def validate_local_plugin(line: int, module: str, path: str):
    if not module:
        raise ValueError(f"local plugin entry at line {line} is missing a module name")
    if not path:
        raise ValueError(f"local plugin entry at line {line} is missing a path")
