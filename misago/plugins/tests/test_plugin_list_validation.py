import pytest

from ..pluginlist import parse_plugins_list


def test_parser_raises_value_error_if_local_plugin_is_missing_path():
    with pytest.raises(ValueError):
        parse_plugins_list("plugin@")


def test_parser_raises_value_error_if_local_plugin_is_missing_module_name():
    with pytest.raises(ValueError):
        parse_plugins_list("@/local/")


def test_parser_raises_value_error_if_plugin_is_repeated():
    with pytest.raises(ValueError):
        parse_plugins_list("plugin\nplugin")


def test_parser_raises_value_error_if_local_plugin_is_repeated():
    with pytest.raises(ValueError):
        parse_plugins_list("plugin@/local/\n@plugin/other/local/")


def test_parser_raises_value_error_if_local_plugin_module_conflicts_with_other_plugin():
    with pytest.raises(ValueError):
        parse_plugins_list("plugin\nplugin@/local/")
