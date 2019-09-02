import os
from typing import List, Optional


def load_plugin_list_if_exists(path: str) -> Optional[List[str]]:
    if not os.path.exists(path):
        return None

    return load_plugin_list(path)


def load_plugin_list(path: str) -> List[str]:
    with open(path, "r") as f:
        data = f.read()
        return parse_plugins_list(data)


def parse_plugins_list(data: str) -> List[str]:
    plugins = []
    for line in data.splitlines():
        plugin = line.strip()
        if not plugin or line.startswith("#"):
            continue
        if plugin not in plugins:
            plugins.append(plugin)
    return plugins
