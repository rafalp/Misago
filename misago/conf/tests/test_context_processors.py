from unittest.mock import Mock

from django.test import TestCase

from misago.cache.versions import get_cache_versions
from misago.core import threadstore

from misago.conf.context_processors import conf
from misago.conf.dynamicsettings import DynamicSettings


class ContextProcessorsTests(TestCase):
    def tearDown(self):
        threadstore.clear()

    def test_db_settings(self):
        """DBSettings are exposed to templates"""
        cache_versions = get_cache_versions()
        mock_request = Mock(settings=DynamicSettings(cache_versions))
        context_settings = conf(mock_request)['settings']
        assert context_settings == mock_request.settings

    def test_preload_settings(self):
        """site configuration is preloaded by middleware"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"SETTINGS": {"')
