import os
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

import pytest
from starlette.datastructures import UploadFile

from .. import tables
from ..conf.cache import SETTINGS_CACHE
from ..conf.dynamicsettings import get_dynamic_settings
from ..database import database
from ..database.testdatabase import create_test_database, teardown_test_database


def pytest_configure():
    create_test_database()


def pytest_unconfigure():
    teardown_test_database()


@pytest.fixture
async def db():
    await database.connect()
    yield database
    await database.disconnect()


@pytest.fixture
def broadcast_publish(mocker):
    return mocker.patch("misago.pubsub.broadcast.publish")


@pytest.fixture
def mock_subscribe(mocker):
    def patch_subscribe(expected_channel: str, message: any):
        async def _mock_subscribe():
            yield Mock(message=str(message))

        class MockSubscribe:
            def __init__(self, *, channel):
                assert expected_channel == channel

            async def __aenter__(self):
                return _mock_subscribe()

            async def __aexit__(self, *args, **kwargs):
                pass

        return mocker.patch("misago.pubsub.broadcast.subscribe", MockSubscribe)

    return patch_subscribe


@pytest.fixture
def cache_versions():
    return {SETTINGS_CACHE: "settings-cache"}


@pytest.fixture
async def cache_version(db):
    query = tables.cache_versions.insert(None).values(
        cache="test_cache", version="version"
    )
    await db.execute(query)
    return {"cache": "test_cache", "version": "version"}


@pytest.fixture
async def other_cache_version(db):
    query = tables.cache_versions.insert(None).values(
        cache="test_other_cache", version="version"
    )
    await db.execute(query)
    return {"cache": "test_other_cache", "version": "version"}


@pytest.fixture
async def dynamic_settings(db, cache_versions):
    return await get_dynamic_settings(cache_versions)


@pytest.fixture
def tmp_media_dir():
    with TemporaryDirectory() as tmp_media_dir:
        with patch("misago.conf.settings._media_root", tmp_media_dir):
            yield tmp_media_dir


TEST_FILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")


@pytest.fixture
def test_files_path():
    return TEST_FILES_PATH


@pytest.fixture
def create_upload_file(test_files_path):
    async def upload_file_factory(filename):
        upload = UploadFile(filename)
        with open(os.path.join(test_files_path, filename), "rb") as fp:
            await upload.write(fp.read())
        return upload

    return upload_file_factory
