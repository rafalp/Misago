import pytest
from faker import Faker
from misago.conftest import db


@pytest.fixture
def faker():
    return Faker()
