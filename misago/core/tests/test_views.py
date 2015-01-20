from django.core.urlresolvers import reverse
from django.test import TestCase


class ForumIndexViewTests(TestCase):
    def test_forum_index_returns_200(self):
        """forum_index view has no show-stoppers"""
        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)


class JavaScriptViewTests(TestCase):
    def test_js_catalog_view_returns_200(self):
        """js catalog view has no show-stoppers"""
        response = self.client.get('/django-i18n.js')
        self.assertEqual(response.status_code, 200)

    def test_preload_data_view_returns_200(self):
        """preload_data view has no show-stoppers"""
        response = self.client.get('/misago-preload-data.js')
        self.assertEqual(response.status_code, 200)
