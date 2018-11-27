from unittest.mock import Mock, PropertyMock, patch

from django.test import TestCase
from django.utils.functional import SimpleLazyObject

from misago.cache.cache import CACHE_NAME
from misago.cache.middleware import cache_versions_middleware


class MiddlewareTests(TestCase):
    def test_middleware_sets_attr_on_request(self):
        get_response = Mock()
        request = Mock()
        cache_versions = PropertyMock()
        type(request).cache_versions = cache_versions
        middleware = cache_versions_middleware(get_response)
        middleware(request)
        cache_versions.assert_called_once()

    def test_attr_set_by_middleware_on_request_is_lazy_object(self):
        get_response = Mock()
        request = Mock()
        cache_versions = PropertyMock()
        type(request).cache_versions = cache_versions
        middleware = cache_versions_middleware(get_response)
        middleware(request)
        attr_value = cache_versions.call_args[0][0]
        assert isinstance(attr_value, SimpleLazyObject)

    def test_middleware_calls_get_response(self):
        get_response = Mock()
        request = Mock()
        middleware = cache_versions_middleware(get_response)
        middleware(request)
        get_response.assert_called_once()

    def test_middleware_is_not_making_db_query(self):
        get_response = Mock()
        request = Mock()
        with self.assertNumQueries(0):
            middleware = cache_versions_middleware(get_response)
            middleware(request)

    def test_middleware_is_not_reading_cache(self):
        get_response = Mock()
        request = Mock()
        middleware = cache_versions_middleware(get_response)
        middleware(request)
