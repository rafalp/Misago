from unittest.mock import Mock

import pytest

from ..environment import get_template_loaders


@pytest.fixture
def patch_package_loader(mocker):
    def mock_loader(module_path, templates_dir):
        return (module_path, templates_dir)

    mocker.patch("misago.template.environment.PackageLoader", mock_loader)


def test_template_loaders_include_misago(mocker, patch_package_loader):
    mocker.patch(
        "misago.template.environment.plugins.get_plugins_with_directory",
        return_value=[],
    )

    loaders = get_template_loaders()
    assert loaders == [("misago.template", "templates")]


def test_template_loaders_include_plugins(mocker, patch_package_loader):
    mocker.patch(
        "misago.template.environment.plugins.get_plugins_with_directory",
        return_value=[(Mock(package_name="test_plugin"), "templates")],
    )

    loaders = get_template_loaders()
    assert loaders == [("test_plugin", "templates"), ("misago.template", "templates")]
