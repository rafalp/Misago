from django.core.urlresolvers import reverse
from django.test import TestCase


class MomentJSCatalogViewTests(TestCase):
    def test_moment_js_catalog_view_returns_200(self):
        """moment.js catalog view has no show-stoppers"""
        with self.settings(LANGUAGE_CODE='en_us'):
            response = self.client.get('/moment-i18n.js')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, "")

        with self.settings(LANGUAGE_CODE='pl_pl'):
            response = self.client.get('/moment-i18n.js')
            self.assertEqual(response.status_code, 200)
            self.assertIn(response.content, "// locale : polish (pl)")


class PreloadJSDataViewTests(TestCase):
    def test_js_catalog_view_returns_200(self):
        """js catalog view has no show-stoppers"""
        response = self.client.get('/django-i18n.js')
        self.assertEqual(response.status_code, 200)


class RedirectViewTests(TestCase):
    urls = 'misago.core.testproject.urls'

    def test_redirect_view(self):
        """redirect view always redirects to home page"""
        response = self.client.get(reverse('test-redirect'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith(reverse('misago:index')))
