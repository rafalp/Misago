import os


PLUGINS_DIR = os.environ.get("MISAGO_PLUGINS") or None


class PluginLoader:
    def __init__(self):
        pass

    def load_plugins(self):
        pass

    def get_plugins_manifests(self):
        pass

    def get_plugins_apps(self):
        pass


plugin_loader = PluginLoader()

if PLUGINS_DIR:
    plugins_dir = os.path(PLUGINS_DIR)
    if plugins_dir.isdir():
        plugin_loader.load_plugins(plugins_dir)
