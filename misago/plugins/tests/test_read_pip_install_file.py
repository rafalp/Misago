from pathlib import Path
from tempfile import TemporaryDirectory

from ..discover import read_pip_install_file


def test_empty_pip_install_file_is_read_to_empty_list():
    with TemporaryDirectory() as plugins_dir:
        pip_install_path = Path(plugins_dir) / "pip-install.txt"
        with open(pip_install_path, "w"):
            pass

        file_contents = read_pip_install_file(pip_install_path)
        assert file_contents == []


def test_pip_install_file_is_read_without_comments_lines():
    with TemporaryDirectory() as plugins_dir:
        pip_install_path = Path(plugins_dir) / "pip-install.txt"
        with open(pip_install_path, "w") as fp:
            fp.writelines(["# comment\n", "other\n"])

        file_contents = read_pip_install_file(pip_install_path)
        assert file_contents == ["other"]


def test_pip_install_file_is_read_without_comments_after_content():
    with TemporaryDirectory() as plugins_dir:
        pip_install_path = Path(plugins_dir) / "pip-install.txt"
        with open(pip_install_path, "w") as fp:
            fp.write("line # comment")

        file_contents = read_pip_install_file(pip_install_path)
        assert file_contents == ["line"]


def test_pip_install_file_is_read_lines_trimmed():
    with TemporaryDirectory() as plugins_dir:
        pip_install_path = Path(plugins_dir) / "pip-install.txt"
        with open(pip_install_path, "w") as fp:
            fp.writelines(["line   \n", "    other\n"])

        file_contents = read_pip_install_file(pip_install_path)
        assert file_contents == ["line", "other"]


def test_pip_install_file_is_read_without_duplicate_lines():
    with TemporaryDirectory() as plugins_dir:
        pip_install_path = Path(plugins_dir) / "pip-install.txt"
        with open(pip_install_path, "w") as fp:
            fp.writelines(["line\n", "other\n", "line\n"])

        file_contents = read_pip_install_file(pip_install_path)
        assert file_contents == ["line", "other"]


def test_pip_install_file_is_read_without_version_data():
    with TemporaryDirectory() as plugins_dir:
        pip_install_path = Path(plugins_dir) / "pip-install.txt"
        with open(pip_install_path, "w") as fp:
            fp.write("line==0.12rc1\n")

        file_contents = read_pip_install_file(pip_install_path)
        assert file_contents == ["line"]


def test_pip_install_file_is_read_with_names_converted_to_package_names():
    with TemporaryDirectory() as plugins_dir:
        pip_install_path = Path(plugins_dir) / "pip-install.txt"
        with open(pip_install_path, "w") as fp:
            fp.write("plugin-name\n")

        file_contents = read_pip_install_file(pip_install_path)
        assert file_contents == ["plugin_name"]


def test_pip_install_file_is_read_with_blank_lines_skipped():
    with TemporaryDirectory() as plugins_dir:
        pip_install_path = Path(plugins_dir) / "pip-install.txt"
        with open(pip_install_path, "w") as fp:
            fp.write("plugin-name\n\nline")

        file_contents = read_pip_install_file(pip_install_path)
        assert file_contents == ["plugin_name", "line"]
