from unittest.mock import Mock

from django.test import TestCase

from misago.conftest import get_cache_versions

from misago.conf.context_processors import conf
from misago.conf.dynamicsettings import DynamicSettings


class ContextProcessorsTests(TestCase):
    def test_request_settings_are_included_in_template_context(self):
        cache_versions = get_cache_versions()
        mock_request = Mock(settings=DynamicSettings(cache_versions))
        context_settings = conf(mock_request)['settings']
        assert context_settings == mock_request.settings

    def test_settings_are_included_in_frontend_context(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"SETTINGS": {"')
