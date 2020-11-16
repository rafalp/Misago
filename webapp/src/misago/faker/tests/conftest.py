import pytest
from faker import Factory


@pytest.fixture
def fake():
    return Factory.create()
