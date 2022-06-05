from ..conf import settings
from .loader import PluginData, PluginsLoader
from .manifest import PluginManifest

__all__ = [
    "PluginData",
    "PluginsLoader",
    "PluginManifest",
    "import_plugins",
    "plugins_loader",
]

plugins_loader = PluginsLoader(settings.plugins_root)


MODULES_TO_IMPORT = ("tables", "plugin", "cli")


def import_plugins():
    for module in MODULES_TO_IMPORT:
        plugins_loader.import_modules_if_exists(module)
