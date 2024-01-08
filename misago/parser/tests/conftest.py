import pytest

from ..factory import create_markdown


@pytest.fixture
def markdown():
    return create_markdown()
