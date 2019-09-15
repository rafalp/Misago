from ..conf import settings
from .loader import PluginLoader


plugins = PluginLoader(settings.enabled_plugins)


MODULES_TO_IMPORT = ("tables", "plugin", "cli")


def import_plugins():
    for module in MODULES_TO_IMPORT:
        plugins.import_module_if_exists(module)
