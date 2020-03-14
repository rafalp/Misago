import pytest
from faker import Faker
from misago.conftest import *  # pylint: disable=wilcard-import


@pytest.fixture
def faker():
    return Faker()
