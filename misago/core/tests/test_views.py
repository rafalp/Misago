from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings


class MomentJSCatalogViewTests(TestCase):
    def test_moment_js_catalog_view_returns_200(self):
        """moment.js catalog view has no show-stoppers"""
        with self.settings(LANGUAGE_CODE='en-us'):
            response = self.client.get('/moment-i18n.js')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, b"")

        with self.settings(LANGUAGE_CODE='pl-pl'):
            response = self.client.get('/moment-i18n.js')
            self.assertContains(response, "// locale : polish (pl)")


class PreloadJSDataViewTests(TestCase):
    def test_js_catalog_view_returns_200(self):
        """js catalog view has no show-stoppers"""
        response = self.client.get('/django-i18n.js')
        self.assertEqual(response.status_code, 200)



@override_settings(ROOT_URLCONF='misago.core.testproject.urls')
class RedirectViewTests(TestCase):
    def test_redirect_view(self):
        """redirect view always redirects to home page"""
        response = self.client.get(reverse('test-redirect'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith(reverse('misago:index')))
