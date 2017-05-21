from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import Client, TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse

from misago.core.testproject.views import mock_custom_403_error_page, mock_custom_404_error_page
from misago.core.utils import encode_json_html
from misago.users.models import AnonymousUser


class CSRFErrorViewTests(TestCase):
    def test_csrf_failure(self):
        """csrf_failure error page has no show-stoppers"""
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(reverse('misago:index'), data={'eric': 'fish'})
        self.assertContains(response, "Request blocked", status_code=403)


@override_settings(ROOT_URLCONF='misago.core.testproject.urls')
class ErrorPageViewsTests(TestCase):
    def test_banned_returns_403(self):
        """banned error page has no show-stoppers"""
        response = self.client.get(reverse('raise-misago-banned'))
        self.assertContains(response, "misago:error-banned", status_code=403)
        self.assertContains(response, encode_json_html("<p>Banned for test!</p>"), status_code=403)

    def test_permission_denied_returns_403(self):
        """permission_denied error page has no show-stoppers"""
        response = self.client.get(reverse('raise-misago-403'))
        self.assertContains(response, "misago:error-403", status_code=403)
        self.assertContains(response, "Page not available", status_code=403)

    def test_page_not_found_returns_404(self):
        """page_not_found error page has no show-stoppers"""
        response = self.client.get(reverse('raise-misago-404'))
        self.assertContains(response, "misago:error-404", status_code=404)
        self.assertContains(response, "Page not found", status_code=404)

    def test_not_allowed_returns_405(self):
        """not allowed error page has no showstoppers"""
        response = self.client.get(reverse('raise-misago-405'))
        self.assertContains(response, "misago:error-405", status_code=405)
        self.assertContains(response, "Wrong way", status_code=405)


@override_settings(ROOT_URLCONF='misago.core.testproject.urlswitherrorhandlers')
class CustomErrorPagesTests(TestCase):
    def setUp(self):
        self.misago_request = RequestFactory().get(reverse('misago:index'))
        self.site_request = RequestFactory().get(reverse('raise-403'))

        self.misago_request.user = AnonymousUser()
        self.site_request.user = AnonymousUser()

        self.misago_request.include_frontend_context = True
        self.site_request.include_frontend_context = True

        self.misago_request.frontend_context = {}
        self.site_request.frontend_context = {}

    def test_shared_403_decorator(self):
        """shared_403_decorator calls correct error handler"""
        response = self.client.get(reverse('raise-misago-403'))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('raise-403'))
        self.assertContains(response, "Custom 403", status_code=403)

        response = mock_custom_403_error_page(self.misago_request, PermissionDenied())
        self.assertNotContains(response, "Custom 403", status_code=403)
        response = mock_custom_403_error_page(self.site_request, PermissionDenied())
        self.assertContains(response, "Custom 403", status_code=403)

    def test_shared_404_decorator(self):
        """shared_404_decorator calls correct error handler"""
        response = self.client.get(reverse('raise-misago-404'))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('raise-404'))
        self.assertContains(response, "Custom 404", status_code=404)

        response = mock_custom_404_error_page(self.misago_request, Http404())
        self.assertNotContains(response, "Custom 404", status_code=404)
        response = mock_custom_404_error_page(self.site_request, Http404())
        self.assertContains(response, "Custom 404", status_code=404)
