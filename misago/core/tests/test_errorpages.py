from django.core.urlresolvers import reverse
from django.test import TestCase


class ErrorPageViewsTests(TestCase):
    urls = 'misago.core.testproject.urls'

    def test_permission_denied_returns_403(self):
        """permission_denied error page has no show-stoppers"""
        response = self.client.get(reverse('raise_misago_403'))
        self.assertEqual(response.status_code, 403)

    def test_page_not_found_returns_404(self):
        """page_not_found error page has no show-stoppers"""
        response = self.client.get(reverse('raise_misago_404'))
        self.assertEqual(response.status_code, 404)


class CustomErrorPagesTests(TestCase):
    urls = 'misago.core.testproject.urlswitherrorhandlers'

    def test_shared_403_decorator(self):
        """shared_403_decorator calls correct error handler"""
        response = self.client.get(reverse('raise_misago_403'))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('raise_403'))
        self.assertEqual(response.status_code, 403)
        self.assertIn("Custom 403", response.content)

    def test_shared_404_decorator(self):
        """shared_404_decorator calls correct error handler"""
        response = self.client.get(reverse('raise_misago_404'))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('raise_404'))
        self.assertEqual(response.status_code, 404)
        self.assertIn("Custom 404", response.content)
