from django.test import TestCase
from misago.core import threadstore
from misago.conf.context_processors import settings
from misago.conf.dbsettings import db_settings


class MockRequest(object):
    pass


class ContextProcessorTests(TestCase):
    serialized_rollback = True

    def tearDown(self):
        threadstore.clear()

    def test_db_settings(self):
        """DBSettings are exposed to templates"""
        mock_request = MockRequest()
        processor_settings = settings(mock_request)['misago_settings'],

        self.assertEqual(id(processor_settings[0]), id(db_settings))
