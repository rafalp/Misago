from ..discovery import discover_plugins


def test_datafaker_plugin_is_discovered(plugins_root):
    plugins = discover_plugins(plugins_root)
    plugins_packages = [plugin.package_name for plugin in plugins]
    print(plugins_packages)
    assert "someplugin" in plugins_packages
