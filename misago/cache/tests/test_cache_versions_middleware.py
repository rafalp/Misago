from unittest.mock import Mock

from django.test import TestCase

from misago.cache.versions import CACHE_NAME
from misago.cache.middleware import cache_versions_middleware


class MiddlewareTests(TestCase):
    def test_middleware_sets_attr_on_request(self):
        get_response = Mock()
        request = Mock()
        middleware = cache_versions_middleware(get_response)
        middleware(request)
        assert request.cache_versions

    def test_middleware_calls_get_response(self):
        get_response = Mock()
        request = Mock()
        middleware = cache_versions_middleware(get_response)
        middleware(request)
        get_response.assert_called_once()
