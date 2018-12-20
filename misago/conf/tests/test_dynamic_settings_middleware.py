from unittest.mock import Mock, PropertyMock, patch

from django.test import TestCase
from django.utils.functional import SimpleLazyObject

from misago.conf.dynamicsettings import DynamicSettings
from misago.conf.middleware import dynamic_settings_middleware


class MiddlewareTests(TestCase):
    def test_middleware_sets_attr_on_request(self):
        get_response = Mock()
        request = Mock()
        settings = PropertyMock()
        type(request).settings = settings
        middleware = dynamic_settings_middleware(get_response)
        middleware(request)
        settings.assert_called_once()

    def test_attr_set_by_middleware_on_request_is_lazy_object(self):
        get_response = Mock()
        request = Mock()
        settings = PropertyMock()
        type(request).settings = settings
        middleware = dynamic_settings_middleware(get_response)
        middleware(request)
        attr_value = settings.call_args[0][0]
        assert isinstance(attr_value, SimpleLazyObject)

    def test_middleware_calls_get_response(self):
        get_response = Mock()
        request = Mock()
        middleware = dynamic_settings_middleware(get_response)
        middleware(request)
        get_response.assert_called_once()

    def test_middleware_is_not_reading_db(self):
        get_response = Mock()
        request = Mock()
        with self.assertNumQueries(0):
            middleware = dynamic_settings_middleware(get_response)
            middleware(request)

    @patch('django.core.cache.cache.get')
    def test_middleware_is_not_reading_cache(self, cache_get):
        get_response = Mock()
        request = Mock()
        middleware = dynamic_settings_middleware(get_response)
        middleware(request)
        cache_get.assert_not_called()