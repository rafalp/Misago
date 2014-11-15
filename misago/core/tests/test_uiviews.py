from copy import copy

from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.test import TestCase

from misago.admin.testutils import AdminTestCase

from misago.core import uiviews


class UIViewDecoratorTests(TestCase):
    def setUp(self):
        self._ui_views = copy(uiviews.UI_VIEWS)

    def tearDown(self):
        uiviews.UI_VIEWS = self._ui_views

    def test_decorator(self):
        """decorator registers view in UI"""
        @uiviews.uiview('bigkahunaburger', 42)
        def fakey_view(request):
            return {'is_tests': True}

        for name, cache_frequency, view in uiviews.UI_VIEWS:
            if (name == 'bigkahunaburger' and cache_frequency == 42 and
                    view == fakey_view):
                break
        else:
            self.fail("uiviews.uiview decorator didn't register uiview")


class UIServerTests(TestCase):
    def test_server_response(self):
        """UI Server returns JSON Response for valid request"""
        headers = {
            'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
            'HTTP_REFERER': 'http://test.com/',
            'HTTP_HOST': 'test.com',
        }
        response = self.client.get(reverse('misago:ui_server'),
                                   **headers)

        self.assertTrue(isinstance(response, JsonResponse))
        self.assertEqual(response.status_code, 200)


class AuthenticatedUIServerTests(AdminTestCase):
    def test_server_response(self):
        """UI Server returns JSON Response for authenticated request"""
        headers = {
            'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
            'HTTP_REFERER': 'http://test.com/',
            'HTTP_HOST': 'test.com',
        }
        response = self.client.get(reverse('misago:ui_server'),
                                   **headers)

        self.assertTrue(isinstance(response, JsonResponse))
        self.assertEqual(response.status_code, 200)
