from unittest.mock import Mock

import pytest


@pytest.fixture
def request_mock(user):
    return Mock(scheme="http", get_host=Mock(return_value="example.com"), user=user)
