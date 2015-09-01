from django.core.urlresolvers import reverse
from django.test import TestCase


class ForumIndexViewTests(TestCase):
    def test_forum_index_returns_200(self):
        """forum_index view has no show-stoppers"""
        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)


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


class NoScriptViewTests(TestCase):
    urls = 'misago.core.testproject.urls'

    def test_noscript_view_returns_200(self):
        """noscript view has no show-stoppers"""
        response = self.client.post(reverse('test_noscript'), {})
        self.assertEqual(response.status_code, 200)

    def test_noscript_view_message_returns_200(self):
        """noscript view with custom message has no show-stoppers"""
        test_message = "Enable JavaScript to roll, Bob!"
        response = self.client.post(reverse('test_noscript'), {
            'message': test_message
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(test_message, response.content)

    def test_noscript_view_title_returns_200(self):
        """noscript view with custom title has no show-stoppers"""
        test_title = "N0p3"
        response = self.client.post(reverse('test_noscript'), {
            'title': test_title
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(test_title, response.content)

    def test_noscript_view_title_message_returns_200(self):
        """noscript view with custom title and message has no show-stoppers"""
        test_title = "N0p3"
        test_message = "Enable JavaScript to roll, Bob!"

        response = self.client.post(reverse('test_noscript'), {
            'title': test_title,
            'message': test_message
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(test_title, response.content)
        self.assertIn(test_message, response.content)
