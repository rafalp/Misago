from ..conf import settings
from .loader import PluginLoader


plugins = PluginLoader(settings.plugins)


MODULES_TO_IMPORT = ("tables", "plugin", "cli", "routes")


def import_plugins():
    for module in MODULES_TO_IMPORT:
        plugins.import_modules_if_exists(module)
