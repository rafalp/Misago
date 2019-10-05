import os
from typing import Dict, List, Optional, Tuple


def load_plugin_list_if_exists(path: str) -> Optional[List[str]]:
    if not os.path.exists(path):
        return None

    return load_plugin_list(path)


def load_plugin_list(path: str) -> List[str]:
    with open(path, "r") as f:
        data = f.read()
        return parse_plugins_list(data)


def parse_plugins_list(data: str) -> List[str]:
    plugins: List[str] = []
    definitions: Dict[str, Tuple[int, str]] = {}

    for line, entry in enumerate(data.splitlines()):
        plugin = entry.strip()

        if "#" in plugin:
            comment_start = plugin.find("#")
            plugin = plugin[:comment_start].strip()
        if not plugin:
            continue

        if plugin in definitions:
            first_line, first_entry = definitions[plugin]
            raise ValueError(
                f"plugin '{plugin}' is listed more than once: "
                f"at line {first_line} ('{first_entry}') and at {line} ('{entry}')"
            )
        definitions[plugin] = line, entry

        plugins.append(plugin)

    return plugins
