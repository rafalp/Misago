from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from ..discover import discover_plugins


@pytest.fixture
def sys_mock(mocker):
    mock = mocker.patch("misago.plugins.discover.sys")
    mock.path = []
    return mock


def test_discover_plugins_returns_empty_list_if_plugins_path_is_empty(sys_mock):
    plugins = discover_plugins("")
    assert plugins == []


def test_discover_plugins_doesnt_update_sys_path_if_plugins_path_is_empty(sys_mock):
    assert not discover_plugins("")
    assert sys_mock.path == []


def test_discover_plugins_returns_empty_list_if_plugins_path_doesnt_exist(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        plugins = discover_plugins(str(Path(plugins_dir) / "doesnt_exist"))
        assert plugins == []


def test_discover_plugins_doesnt_update_sys_path_if_plugins_path_doesnt_exist(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        assert not discover_plugins(str(Path(plugins_dir) / "doesnt_exist"))
        assert sys_mock.path == []


def test_discover_plugins_returns_empty_list_if_plugins_dir_is_empty(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        plugins = discover_plugins(plugins_dir)
        assert plugins == []


def test_discover_plugins_doesnt_update_sys_path_if_plugins_dir_is_empty(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        assert not discover_plugins(plugins_dir)
        assert sys_mock.path == []


def create_plugin(plugins_dir: str, dir_name: str, package_name: str) -> Path:
    plugin_path = Path(plugins_dir) / dir_name
    plugin_path.mkdir()

    plugin_package_path = plugin_path / package_name
    plugin_package_path.mkdir()

    plugin_init_path = plugin_package_path / "__init__.py"
    plugin_init_path.touch()

    plugin_misago_marker_path = plugin_package_path / "misago_plugin.py"
    plugin_misago_marker_path.touch()

    return plugin_misago_marker_path


def test_discover_plugins_returns_plugins_list(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        create_plugin(plugins_dir, "mock-plugin", "mock_plugin")
        create_plugin(plugins_dir, "other-plugin", "other_plugin")

        plugins = discover_plugins(plugins_dir)
        assert plugins == ["mock_plugin", "other_plugin"]


def test_discover_plugins_adds_plugins_to_python_path(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        create_plugin(plugins_dir, "mock-plugin", "mock_plugin")
        create_plugin(plugins_dir, "other-plugin", "other_plugin")

        assert discover_plugins(plugins_dir)
        assert sys_mock.path == [
            f"{plugins_dir}/mock-plugin",
            f"{plugins_dir}/other-plugin",
        ]


def test_discover_plugins_doesnt_create_duplicates_in_python_path(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        create_plugin(plugins_dir, "mock-plugin", "mock_plugin")
        create_plugin(plugins_dir, "other-plugin", "other_plugin")

        sys_mock.path.append(f"{plugins_dir}/mock-plugin")

        assert discover_plugins(plugins_dir)
        assert sys_mock.path == [
            f"{plugins_dir}/mock-plugin",
            f"{plugins_dir}/other-plugin",
        ]


def test_discover_plugins_skips_packages_without_misago_plugin_py(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        create_plugin(plugins_dir, "mock-plugin", "mock_plugin")

        other_plugin = create_plugin(plugins_dir, "other-plugin", "other_plugin")
        other_plugin.unlink()

        plugins = discover_plugins(plugins_dir)
        assert plugins == ["mock_plugin"]
        assert sys_mock.path == [f"{plugins_dir}/mock-plugin"]


def test_discover_plugins_returns_plugins_apps_sorted_by_name(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        create_plugin(plugins_dir, "mock-plugin", "mock_plugin")
        create_plugin(plugins_dir, "other-plugin", "alpha_plugin")

        plugins = discover_plugins(plugins_dir)
        assert plugins == ["alpha_plugin", "mock_plugin"]


def test_discover_plugins_adds_plugins_to_python_path_ordered_by_app_name(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        create_plugin(plugins_dir, "mock-plugin", "mock_plugin")
        create_plugin(plugins_dir, "other-plugin", "alpha_plugin")

        assert discover_plugins(plugins_dir)
        assert sys_mock.path == [
            f"{plugins_dir}/other-plugin",
            f"{plugins_dir}/mock-plugin",
        ]


def test_discover_plugins_skips_plugins_without_init(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        create_plugin(plugins_dir, "mock-plugin", "mock_plugin")

        invalid_plugin_path = create_plugin(plugins_dir, "invalid-plugin", "invalid")
        invalid_plugin_path_init = invalid_plugin_path.parent / "__init__.py"
        invalid_plugin_path_init.unlink()

        plugins = discover_plugins(plugins_dir)
        assert plugins == ["mock_plugin"]
        assert sys_mock.path == [f"{plugins_dir}/mock-plugin"]


def create_pip_install(plugins_dir: str, contents: list[str]):
    with open(Path(plugins_dir) / "pip-install.txt", "w") as fp:
        fp.write("\n".join(contents))


@pytest.mark.xfail(reason="requires misago-pypi-plugin installed to pass")
def test_discover_plugins_reads_plugins_from_pip_install_if_it_exists(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        create_pip_install(plugins_dir, ["misago-pypi-plugin"])

        plugins = discover_plugins(plugins_dir)
        assert plugins == ["misago_pypi_plugin"]
        assert sys_mock.path == []


@pytest.mark.xfail(reason="requires misago-pypi-plugin installed to pass")
def test_discover_plugins_skips_pip_install_entries_that_arent_installed(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        create_pip_install(plugins_dir, ["misago-pypi-plugin", "misago-other-plugin"])

        plugins = discover_plugins(plugins_dir)
        assert plugins == ["misago_pypi_plugin"]
        assert sys_mock.path == []


@pytest.mark.xfail(reason="requires misago-pypi-plugin installed to pass")
def test_discover_plugins_skips_pip_install_entries_that_arent_misago_plugins(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        create_pip_install(plugins_dir, ["misago-pypi-plugin", "django"])

        plugins = discover_plugins(plugins_dir)
        assert plugins == ["misago_pypi_plugin"]
        assert sys_mock.path == []


@pytest.mark.xfail(reason="requires misago-pypi-plugin installed to pass")
def test_discover_plugins_skips_pip_install_if_its_directory(sys_mock):
    with TemporaryDirectory() as plugins_dir:
        pip_install_path = Path(plugins_dir) / "pip-install.txt"
        pip_install_path.mkdir()

        plugins = discover_plugins(plugins_dir)
        assert plugins == []
        assert sys_mock.path == []
