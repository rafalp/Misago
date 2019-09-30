from unittest.mock import Mock

from ..loader import PluginLoader


def test_loader_loads_plugins_list_from_given_path(mocker):
    list_path = "/test_list_path/plugins.txt"
    list_mock = mocker.patch(
        "misago.plugins.loader.load_plugin_list_if_exists", return_value=None
    )
    PluginLoader(list_path)
    list_mock.assert_called_once_with(list_path)


def test_loader_is_not_loading_plugins_list_if_path_is_not_set(mocker):
    list_mock = mocker.patch(
        "misago.plugins.loader.load_plugin_list_if_exists", return_value=None
    )
    PluginLoader(None)
    list_mock.assert_not_called()


def test_loader_is_not_loading_plugins_list_if_path_is_empty_str(mocker):
    list_mock = mocker.patch(
        "misago.plugins.loader.load_plugin_list_if_exists", return_value=None
    )
    PluginLoader("")
    list_mock.assert_not_called()


def test_loader_creates_plugin_instance_for_plugin_name(mocker):
    plugin_name = "plugin"
    mocker.patch(
        "misago.plugins.loader.load_plugin_list_if_exists", return_value=[plugin_name]
    )
    plugin = mocker.patch("misago.plugins.loader.Plugin")
    PluginLoader("/plugins/path/")
    plugin.assert_called_once_with(plugin_name)


def test_loader_is_not_adding_non_local_plugin_to_sys_path(mocker):
    plugin_name = "plugin"

    mocker.patch(
        "misago.plugins.loader.load_plugin_list_if_exists", return_value=[plugin_name]
    )
    path_mock = mocker.patch("sys.path", Mock(append=Mock()))
    plugin = mocker.patch("misago.plugins.loader.Plugin")

    PluginLoader("/plugins/path/")
    path_mock.append.assert_not_called()
    plugin.assert_called_once_with("plugin")


def test_loader_adds_local_plugin_path_to_sys_path(mocker):
    plugin_name = "plugin@/local-path/"

    mocker.patch(
        "misago.plugins.loader.load_plugin_list_if_exists", return_value=[plugin_name]
    )
    path_mock = mocker.patch("sys.path", Mock(append=Mock()))
    plugin = mocker.patch("misago.plugins.loader.Plugin")

    PluginLoader("/plugins/path/")
    path_mock.append.assert_called_once_with("/local-path/")
    plugin.assert_called_once_with("plugin")
