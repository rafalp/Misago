from io import BytesIO
import os

import pytest

from ..store import (
    delete_media_file,
    delete_media_directory,
    make_media_directory,
    make_media_path,
    media_file_exists,
    store_media_file,
)


def test_media_path_can_be_created(mock_media_dir):
    media_path = make_media_path("test/file.txt")
    assert media_path.startswith(mock_media_dir)
    assert media_path.endswith("test/file.txt")


def test_media_path_creation_fails_if_path_is_relative(mock_media_dir):
    with pytest.raises(ValueError):
        make_media_path("./file.txt")

    with pytest.raises(ValueError):
        make_media_path("../file.txt")


def test_media_file_can_be_stored_and_accessed(mock_media_dir):
    test_file = BytesIO("Hello world!".encode("utf-8"))

    store_media_file(test_file, "test.txt")
    assert media_file_exists("test.txt")

    with open(make_media_path("test.txt"), "r") as fp:
        file_data = fp.read()
        assert file_data == "Hello world!"


def test_media_file_can_be_stored_in_dir_and_accessed(mock_media_dir):
    test_file = BytesIO("Hello world!".encode("utf-8"))

    store_media_file(test_file, "testdir/test.txt")
    assert media_file_exists("testdir/test.txt")

    with open(make_media_path("testdir/test.txt"), "r") as fp:
        file_data = fp.read()
        assert file_data == "Hello world!"


def test_media_dirs_can_be_created(mock_media_dir):
    dirnames = "some/test/avatars"
    make_media_directory(dirnames)
    assert os.path.isdir(make_media_path(dirnames))


def test_creating_already_existing_media_dirs_is_not_error(mock_media_dir):
    dirnames = "some/test/avatars"
    make_media_directory(dirnames)
    make_media_directory(dirnames)
    assert os.path.isdir(make_media_path(dirnames))


def test_media_file_can_be_removed(mock_media_dir):
    test_file = BytesIO("Hello world!".encode("utf-8"))

    store_media_file(test_file, "test.txt")
    assert media_file_exists("test.txt")
    delete_media_file("test.txt")
    assert not media_file_exists("test.txt")


def test_media_file_in_dir_can_be_removed(mock_media_dir):
    test_file = BytesIO("Hello world!".encode("utf-8"))

    store_media_file(test_file, "testdir/test.txt")
    assert media_file_exists("testdir/test.txt")
    delete_media_file("testdir/test.txt")
    assert not media_file_exists("testdir/test.txt")


def test_media_dir_can_be_removed(mock_media_dir):
    test_file = BytesIO("Hello world!".encode("utf-8"))

    store_media_file(test_file, "testdir/test.txt")
    assert media_file_exists("testdir/test.txt")
    assert os.path.isdir(make_media_path("testdir"))

    delete_media_directory("testdir")
    assert not media_file_exists("testdir/test.txt")
    assert not os.path.isdir(make_media_path("testdir"))
