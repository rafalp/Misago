from unittest.mock import Mock

import pytest


@pytest.fixture
def request_mock():
    return Mock(state=Mock(request=Mock(), cache_versions=Mock(), settings=Mock()))
