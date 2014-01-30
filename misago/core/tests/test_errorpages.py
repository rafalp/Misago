from django.core.urlresolvers import reverse
from django.test import TestCase
from misago.core import errorpages


class ErrorPageViewsTests(TestCase):
    def setUp(self):
        response = self.client.get(reverse('forum_index'))
        self.request = response.request

    def test_permission_denied_returns_403(self):
        """permission_denied error page has no show-stoppers"""
        response = errorpages.permission_denied(self.request)
        self.assertEqual(response.status_code, 403)

    def test_page_not_found_returns_404(self):
        """page_not_found error page has no show-stoppers"""
        response = errorpages.page_not_found(self.request)
        self.assertEqual(response.status_code, 404)
