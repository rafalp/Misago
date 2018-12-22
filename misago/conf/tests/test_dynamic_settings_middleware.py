from unittest.mock import Mock, PropertyMock

import pytest

from django.utils.functional import SimpleLazyObject

from misago.conf.middleware import dynamic_settings_middleware


@pytest.fixture
def get_response():
    return Mock()


@pytest.fixture
def settings():
    return PropertyMock()


@pytest.fixture
def request_mock(settings):
    request = Mock()
    type(request).settings = settings
    return request


def test_middleware_sets_attr_on_request(db, get_response, request_mock, settings):
    middleware = dynamic_settings_middleware(get_response)
    middleware(request_mock)
    settings.assert_called_once()


def test_attr_set_by_middleware_on_request_is_lazy_object(
    db, get_response, request_mock, settings
):
    middleware = dynamic_settings_middleware(get_response)
    middleware(request_mock)
    attr_value = settings.call_args[0][0]
    assert isinstance(attr_value, SimpleLazyObject)


def test_middleware_calls_get_response(db, get_response, request_mock):
    middleware = dynamic_settings_middleware(get_response)
    middleware(request_mock)
    get_response.assert_called_once()


def test_middleware_is_not_reading_db(
    db, get_response, request_mock, django_assert_num_queries
):
    with django_assert_num_queries(0):
        middleware = dynamic_settings_middleware(get_response)
        middleware(request_mock)


def test_middleware_is_not_reading_cache(db, mocker, get_response, request_mock):
    cache_get = mocker.patch("django.core.cache.cache.get")
    middleware = dynamic_settings_middleware(get_response)
    middleware(request_mock)
    cache_get.assert_not_called()
