import pytest
from faker import Faker
from misago.conftest import (  # pylint: disable=unused-import
    categories,
    category,
    db,
    pytest_configure,
    pytest_unconfigure,
    thread_and_post,
    thread,
    user,
    user_password,
)


@pytest.fixture
def faker():
    return Faker()
