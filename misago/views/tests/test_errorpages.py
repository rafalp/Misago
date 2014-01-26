from django.test import TestCase
from django.test.client import Client
from misago.views import errorpages


class ErrorPageViewsTests(TestCase):
    def setUp(self):
        c = Client()
        response = c.get(reverse('forum_index'))
        self.request = response.request

    def test_permission_denied_returns_200(self):
        """permission_denied error page has no show-stoppers"""
        response = errorpages.permission_denied(self.request)
        self.assertEqual(response.status_code, 200)

    def test_page_not_found_returns_200(self):
        """page_not_found error page has no show-stoppers"""
        response = errorpages.page_not_found(self.request)
        self.assertEqual(response.status_code, 200)
