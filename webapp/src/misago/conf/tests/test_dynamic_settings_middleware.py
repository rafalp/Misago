from unittest.mock import Mock

import pytest
from django.utils.functional import SimpleLazyObject

from ..middleware import dynamic_settings_middleware


@pytest.fixture
def get_response():
    return Mock()


class PlainRequest:
    pass


@pytest.fixture
def plain_request():
    return PlainRequest()


def test_middleware_sets_attr_on_request(db, get_response, plain_request):
    middleware = dynamic_settings_middleware(get_response)
    middleware(plain_request)
    assert hasattr(plain_request, "settings")


def test_attr_set_by_middleware_on_request_is_lazy_object(
    db, get_response, plain_request
):
    middleware = dynamic_settings_middleware(get_response)
    middleware(plain_request)
    assert isinstance(plain_request.settings, SimpleLazyObject)


def test_middleware_calls_get_response(db, get_response, plain_request):
    middleware = dynamic_settings_middleware(get_response)
    middleware(plain_request)
    get_response.assert_called_once()


def test_middleware_is_not_reading_from_db(
    db, get_response, plain_request, django_assert_num_queries
):
    with django_assert_num_queries(0):
        middleware = dynamic_settings_middleware(get_response)
        middleware(plain_request)


def test_middleware_is_not_reading_from_cache(db, mocker, get_response, plain_request):
    cache_get = mocker.patch("django.core.cache.cache.get")
    middleware = dynamic_settings_middleware(get_response)
    middleware(plain_request)
    cache_get.assert_not_called()
