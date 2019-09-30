import pytest

from ..plugin import Plugin


@pytest.fixture
def plugin():
    return Plugin("misago.plugins.tests.plugin")


@pytest.fixture
def package_plugin():
    return Plugin("misago.plugins.tests.package_plugin")


def test_plugin_is_imported(plugin):
    assert plugin.get_main_module().SIMPLE_PLUGIN


def test_package_plugin_is_imported(package_plugin):
    assert package_plugin.get_main_module().PACKAGE_PLUGIN


def test_existing_plugin_module_is_safely_imported(package_plugin):
    assert package_plugin.import_module_if_exists("submodule").SUBMODULE


def test_none_is_returned_if_nonexisting_plugin_module_is_safely_imported(
    package_plugin
):
    assert package_plugin.import_module_if_exists("not_exists") is None


def test_module_is_not_imported_to_test_its_existence(mocker, package_plugin):
    mocker.patch("misago.plugins.plugin.import_module")
    package_plugin.import_module_if_exists("submodule_with_error")


def test_none_is_returned_module_is_safely_imported_from_non_package_plugin(plugin):
    assert plugin.import_module_if_exists("submodule") is None


def test_exception_is_raised_if_nonexisting_plugin_module_is_unsafely_imported(
    package_plugin
):
    with pytest.raises(ImportError):
        package_plugin.import_module("not_exists")


def test_exception_is_raised_if_plugin_module_is_unsafely_imported_from_module_plugin(
    plugin
):
    with pytest.raises(ImportError):
        plugin.import_module("submodule")
