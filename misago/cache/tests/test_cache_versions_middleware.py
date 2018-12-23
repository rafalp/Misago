from unittest.mock import Mock

import pytest

from ..middleware import cache_versions_middleware


@pytest.fixture
def get_response():
    return Mock()


@pytest.fixture
def request_mock():
    return Mock()


def test_middleware_sets_attr_on_request(db, get_response, request_mock):
    middleware = cache_versions_middleware(get_response)
    middleware(request_mock)
    assert request_mock.cache_versions


def test_middleware_calls_get_response(db, get_response, request_mock):
    middleware = cache_versions_middleware(get_response)
    middleware(request_mock)
    get_response.assert_called_once()
