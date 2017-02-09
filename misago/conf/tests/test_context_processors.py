from django.test import TestCase

from misago.conf.context_processors import settings
from misago.conf.dbsettings import db_settings
from misago.core import threadstore


class MockRequest(object):
    pass


class ContextProcessorsTests(TestCase):
    def tearDown(self):
        threadstore.clear()

    def test_db_settings(self):
        """DBSettings are exposed to templates"""
        mock_request = MockRequest()
        processor_settings = settings(mock_request)['misago_settings'],

        self.assertEqual(id(processor_settings[0]), id(db_settings))

    def test_preload_settings(self):
        """site configuration is preloaded by middleware"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"SETTINGS": {"')
