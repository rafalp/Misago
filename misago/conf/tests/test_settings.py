from django.conf import settings as dj_settings
from django.test import TestCase
from misago.conf.gateway import settings as gateway
from misago.conf.dbsettings import db_settings


class DBSettingsTests(TestCase):
    def test_get_existing_setting(self):
        """forum_name is defined"""
        self.assertEqual(db_settings.forum_name, 'Misago')

        with self.assertRaises(AttributeError):
            db_settings.MISAGO_MAILER_BATCH_SIZE


class GatewaySettingsTests(TestCase):
    def test_get_existing_setting(self):
        """forum_name is defined"""
        self.assertEqual(gateway.forum_name, db_settings.forum_name)
        self.assertEqual(gateway.MISAGO_MAILER_BATCH_SIZE,
                         dj_settings.MISAGO_MAILER_BATCH_SIZE)

        with self.assertRaises(AttributeError):
            gateway.LoremIpsum
