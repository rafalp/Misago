import os
from unittest.mock import Mock

from ..loader import PluginsLoader


def test_loader_discovers_plugins_in_given_path(mocker, plugins_root):
    discover_mock = mocker.patch(
        "misago.plugins.loader.discover_plugins", return_value=[]
    )
    PluginsLoader(plugins_root)
    discover_mock.assert_called_once_with(plugins_root)


def test_loader_discovers_admin_plugins_in_given_path(mocker, plugins_root):
    discover_mock = mocker.patch(
        "misago.plugins.loader.discover_admin_plugins", return_value=[]
    )
    PluginsLoader(plugins_root)
    discover_mock.assert_called_once_with(plugins_root)


def test_loader_discovers_client_plugins_in_given_path(mocker, plugins_root):
    discover_mock = mocker.patch(
        "misago.plugins.loader.discover_client_plugins", return_value=[]
    )
    PluginsLoader(plugins_root)
    discover_mock.assert_called_once_with(plugins_root)


def test_loader_is_not_discovering_plugins_if_path_is_not_set(mocker):
    discover_mock = mocker.patch(
        "misago.plugins.loader.discover_plugins", return_value=[]
    )
    PluginsLoader(None)
    discover_mock.assert_not_called()


def test_loader_is_not_discovering_plugins_list_if_path_is_empty_str(mocker):
    discover_mock = mocker.patch(
        "misago.plugins.loader.discover_plugins", return_value=[]
    )
    PluginsLoader("")
    discover_mock.assert_not_called()


def test_loader_adds_plugin_path_to_sys_path(mocker, plugins_root):
    mocker.patch(
        "misago.plugins.plugin.Plugin.import_manifest", Mock(return_value=None)
    )
    path_mock = mocker.patch("sys.path", Mock(append=Mock()))

    PluginsLoader(plugins_root)
    path_mock.append.assert_called()


def test_loader_returns_plugins_data(plugins_root):
    loader = PluginsLoader(plugins_root)
    plugins_data = loader.get_plugins_data()
    assert plugins_data


def test_loader_reads_plugin_data_from_its_manifest(plugins_root):
    loader = PluginsLoader(plugins_root)
    plugins_data = loader.get_plugins_data()
    assert plugins_data

    plugins_data_dict = {plugin.directory: plugin for plugin in plugins_data}
    manifest_plugin = plugins_data_dict.get("manifest_plugin")
    assert manifest_plugin
    assert manifest_plugin.name == "Mock Plugin"
    assert manifest_plugin.description == "Mock plugin for testing"
    assert manifest_plugin.license == "BSD-3"
    assert manifest_plugin.icon == "fas fa-dice"
    assert manifest_plugin.color == "#0466c8"
    assert manifest_plugin.version == "0.1.0"
    assert manifest_plugin.author == "John Doe"
    assert manifest_plugin.homepage == "https://misago-project.org"
    assert manifest_plugin.repo == "https://github.com/rafalp/misago"
    assert manifest_plugin.directory == "manifest_plugin"
    assert manifest_plugin.admin is False
    assert manifest_plugin.client is False


def test_loader_sets_empty_plugin_data_for_plugin_without_manifest(plugins_root):
    loader = PluginsLoader(plugins_root)
    plugins_data = loader.get_plugins_data()
    assert plugins_data

    plugins_data_dict = {plugin.directory: plugin for plugin in plugins_data}

    some_plugin = plugins_data_dict.get("some_plugin")
    assert some_plugin
    assert some_plugin.name == "some_plugin"
    assert some_plugin.description is None
    assert some_plugin.license is None
    assert some_plugin.icon is None
    assert some_plugin.color is None
    assert some_plugin.version is None
    assert some_plugin.author is None
    assert some_plugin.homepage is None
    assert some_plugin.repo is None
    assert some_plugin.directory == "some_plugin"
    assert some_plugin.admin is True
    assert some_plugin.client is False


def test_loader_sets_admin_and_client_plugin_data(plugins_root):
    loader = PluginsLoader(plugins_root)
    plugins_data = loader.get_plugins_data()
    assert plugins_data

    plugins_data_dict = {plugin.directory: plugin for plugin in plugins_data}

    admin_plugin = plugins_data_dict.get("admin_plugin")
    assert admin_plugin
    assert admin_plugin.admin is True
    assert admin_plugin.client is False

    client_plugin = plugins_data_dict.get("client_plugin")
    assert client_plugin
    assert client_plugin.admin is False
    assert client_plugin.client is True


def test_loader_imports_plugin_module_if_it_exists(plugins_root):
    loader = PluginsLoader(plugins_root)
    modules = loader.import_modules_if_exists("submodule")
    assert len(modules) == 1
    assert modules[0][0].directory_name == "some_plugin"
    assert modules[0][0].package_name == "someplugin"
    assert modules[0][1].SUBMODULE is True


def test_loader_returns_empty_list_if_plugin_module_didnt_exist(plugins_root):
    loader = PluginsLoader(plugins_root)
    modules = loader.import_modules_if_exists("notexisting")
    assert modules == []  # pylint: disable=use-implicit-booleaness-not-comparison


def test_loader_returns_list_of_plugins_with_directory(plugins_root):
    loader = PluginsLoader(plugins_root)
    dirs = loader.get_plugins_with_directory("somedir")
    assert len(dirs) == 1
    assert dirs[0][0].directory_name == "some_plugin"
    assert dirs[0][0].package_name == "someplugin"
    assert dirs[0][1] == os.path.join(
        plugins_root, "some_plugin", "someplugin", "somedir"
    )


def test_loader_returns_empty_list_if_plugin_didnt_have_directory(plugins_root):
    loader = PluginsLoader(plugins_root)
    dirs = loader.get_plugins_with_directory("notexisting")
    assert dirs == []  # pylint: disable=use-implicit-booleaness-not-comparison
