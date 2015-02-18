from django.conf import settings
from django.test import TestCase

from misago.core.middleware.embercliredirects import (
    EmberCLIRedirectsMiddleware)


class MockRequest(object):
    def __init__(self, origin):
        self.META = {'HTTP_ORIGIN': origin}


class MockResponse(object):
    def __init__(self, location, code=301):
        self.status_code = code
        self._dict = {'location': location}

    def __setitem__(self, key, item):
        self._dict[key] = item

    def __getitem__(self, key):
        return self._dict[key]


class EmberCLIRedirectsMiddlewareTests(TestCase):
    def test_process_response_rewrites_redirect(self):
        """process_response rewrites redirect"""
        middleware = EmberCLIRedirectsMiddleware()

        request = MockRequest(settings.MISAGO_EMBER_CLI_ORIGIN)

        url = '/thread/bob-boberson-rules-1/'
        response = MockResponse(url, 301)

        with self.settings(DEBUG=True):
            response = MockResponse(url, 301)

            middleware.process_response(request, response)
            self.assertTrue(response['location'].startswith(
                settings.MISAGO_EMBER_CLI_ORIGIN))
            self.assertTrue(response['location'].endswith(url))

        with self.settings(DEBUG=False):
            response = MockResponse(url, 301)

            middleware.process_response(request, response)
            self.assertFalse(response['location'].startswith(
                settings.MISAGO_EMBER_CLI_ORIGIN))
            self.assertTrue(response['location'].endswith(url))

        with self.settings(MISAGO_EMBER_CLI_ORIGIN=''):
            response = MockResponse(url, 301)

            middleware.process_response(request, response)
            self.assertFalse(response['location'].startswith(
                settings.MISAGO_EMBER_CLI_ORIGIN))
            self.assertTrue(response['location'].endswith(url))

    def test_is_ember_cli_request(self):
        """is_ember_cli_request test works"""
        middleware = EmberCLIRedirectsMiddleware()

        valid_request = MockRequest(settings.MISAGO_EMBER_CLI_ORIGIN)
        self.assertTrue(middleware.is_ember_cli_request(valid_request))

        invalid_request = MockRequest('http://somewhere.com/some_page.html')
        self.assertFalse(middleware.is_ember_cli_request(invalid_request))

    def rewrite_http_redirect_url(self):
        """rewrite_http_redirect_url prepents CLI host to URL"""
        middleware = EmberCLIRedirectsMiddleware()

        url = '/thread/bob-boberson-rules-1/'
        rewrited_url = middleware.rewrite_http_redirect_url(url)

        self.assertTrue(rewrited_url.startswith(
            settings.MISAGO_EMBER_CLI_ORIGIN))
        self.assertTrue(rewrited_url.endswith(url))
