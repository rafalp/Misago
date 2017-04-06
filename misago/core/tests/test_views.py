from django.test import TestCase, override_settings
from django.urls import reverse


class CoreViewsTests(TestCase):
    def test_js_catalog_view_returns_200(self):
        """js catalog view has no show-stoppers"""
        response = self.client.get('/django-i18n.js')
        self.assertEqual(response.status_code, 200)

    def test_robots_txt_returns_200(self):
        """robots.txt has no showstoppers"""
        response = self.client.get('/robots.txt')
        self.assertEqual(response['Content-type'], 'text/plain')
        self.assertContains(response, '/api/')


@override_settings(ROOT_URLCONF='misago.core.testproject.urls')
class RedirectViewTests(TestCase):
    def test_redirect_view(self):
        """redirect view always redirects to home page"""
        response = self.client.get(reverse('test-redirect'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith(reverse('misago:index')))
