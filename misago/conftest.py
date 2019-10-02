import pytest

from .database import database
from .database.testdatabase import create_test_database, teardown_test_database


def pytest_configure():
    create_test_database()


def pytest_unconfigure():
    teardown_test_database()


@pytest.fixture(scope="function")
async def db():
    async with database as connection:
        yield connection
