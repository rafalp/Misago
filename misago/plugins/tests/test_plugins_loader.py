import os
from unittest.mock import Mock

from ..loader import PluginLoader


def test_loader_discovers_plugins_in_given_path(mocker, plugins_root):
    discover_mock = mocker.patch(
        "misago.plugins.loader.discover_plugins", return_value=[]
    )
    PluginLoader(plugins_root)
    discover_mock.assert_called_once_with(plugins_root)


def test_loader_is_not_discovering_plugins_if_path_is_not_set(mocker):
    discover_mock = mocker.patch(
        "misago.plugins.loader.discover_plugins", return_value=[]
    )
    PluginLoader(None)
    discover_mock.assert_not_called()


def test_loader_is_not_discovering_plugins_list_if_path_is_empty_str(mocker):
    discover_mock = mocker.patch(
        "misago.plugins.loader.discover_plugins", return_value=[]
    )
    PluginLoader("")
    discover_mock.assert_not_called()


def test_loader_adds_plugin_path_to_sys_path(mocker, plugins_root):
    path_mock = mocker.patch("sys.path", Mock(append=Mock()))
    PluginLoader(plugins_root)
    path_mock.append.assert_called_once()


def test_loader_imports_plugin_module_if_it_exists(plugins_root):
    loader = PluginLoader(plugins_root)
    modules = loader.import_modules_if_exists("submodule")
    assert len(modules) == 1
    assert modules[0][0].package_name == "someplugin"
    assert modules[0][1].SUBMODULE is True


def test_loader_returns_empty_list_if_plugin_module_didnt_exist(plugins_root):
    loader = PluginLoader(plugins_root)
    modules = loader.import_modules_if_exists("notexisting")
    assert modules == []  # pylint: disable=use-implicit-booleaness-not-comparison


def test_loader_returns_list_of_plugins_with_directory(plugins_root):
    loader = PluginLoader(plugins_root)
    dirs = loader.get_plugins_with_directory("somedir")
    assert len(dirs) == 1
    assert dirs[0][0].package_name == "someplugin"
    assert dirs[0][1] == os.path.join(
        plugins_root, "some_plugin", "someplugin", "somedir"
    )


def test_loader_returns_empty_list_if_plugin_didnt_have_directory(plugins_root):
    loader = PluginLoader(plugins_root)
    dirs = loader.get_plugins_with_directory("notexisting")
    assert dirs == []  # pylint: disable=use-implicit-booleaness-not-comparison
