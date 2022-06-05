from ..discover import discover_admin_plugins, discover_client_plugins, discover_plugins


def test_mock_plugin_is_discovered(plugins_root):
    plugins = discover_plugins(plugins_root)
    plugins_packages = [plugin.package_name for plugin in plugins]
    assert "someplugin" in plugins_packages


def test_admin_only_mock_plugin_with_admin_is_discovered(plugins_root):
    plugins = discover_admin_plugins(plugins_root)
    assert "admin_plugin" in plugins


def test_client_only_mock_plugin_with_admin_is_discovered(plugins_root):
    plugins = discover_client_plugins(plugins_root)
    assert "client_plugin" in plugins
