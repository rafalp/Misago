from django.conf import settings
from django.test import TestCase
from django.urls import reverse


class JsI18nUrlTests(TestCase):
    def test_js_i18n_url_cache_buster(self):
        """js i18n catalog link has cachebuster with lang code"""
        url = '{}?{}'.format(reverse('django-i18n'), settings.LANGUAGE_CODE)

        response = self.client.get(reverse('misago:index'))
        self.assertContains(response, url)
