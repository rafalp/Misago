from django.apps import apps
from django.conf import settings as dj_settings
from django.test import TestCase

from misago.conf.dbsettings import db_settings
from misago.conf.gateway import settings as gateway
from misago.conf.migrationutils import migrate_settings_group
from misago.core import threadstore
from misago.core.cache import cache


class DBSettingsTests(TestCase):
    def test_get_existing_setting(self):
        """forum_name is defined"""
        self.assertEqual(db_settings.forum_name, 'Misago')

        with self.assertRaises(AttributeError):
            db_settings.MISAGO_MAILER_BATCH_SIZE


class GatewaySettingsTests(TestCase):
    def tearDown(self):
        cache.clear()
        threadstore.clear()

    def test_get_existing_setting(self):
        """forum_name is defined"""
        self.assertEqual(gateway.forum_name, db_settings.forum_name)
        self.assertEqual(gateway.MISAGO_MAILER_BATCH_SIZE,
                         dj_settings.MISAGO_MAILER_BATCH_SIZE)

        with self.assertRaises(AttributeError):
            gateway.LoremIpsum

    def test_setting_public(self):
        """get_public_settings returns public settings"""
        test_group = {
            'key': 'test_group',
            'name': "Test settings",
            'description': "Those are test settings.",
            'settings': (
                {
                    'setting': 'fish_name',
                    'name': "Fish's name",
                    'value': "Public Eric",
                    'field_extra': {
                            'min_length': 2,
                            'max_length': 255
                        },
                    'is_public': True
                },
                {
                    'setting': 'private_fish_name',
                    'name': "Fish's name",
                    'value': "Private Eric",
                    'field_extra': {
                            'min_length': 2,
                            'max_length': 255
                        },
                    'is_public': False
                },
            )
        }

        migrate_settings_group(apps, test_group)

        self.assertEqual(gateway.fish_name, 'Public Eric')
        self.assertEqual(gateway.private_fish_name, 'Private Eric')

        public_settings = gateway.get_public_settings().keys()
        self.assertIn('fish_name', public_settings)
        self.assertNotIn('private_fish_name', public_settings)


    def test_setting_lazy(self):
        """lazy settings work"""
        test_group = {
            'key': 'test_group',
            'name': "Test settings",
            'description': "Those are test settings.",
            'settings': (
                {
                    'setting': 'fish_name',
                    'name': "Fish's name",
                    'value': "Greedy Eric",
                    'field_extra': {
                            'min_length': 2,
                            'max_length': 255
                        },
                    'is_lazy': False
                },
                {
                    'setting': 'lazy_fish_name',
                    'name': "Fish's name",
                    'value': "Lazy Eric",
                    'field_extra': {
                            'min_length': 2,
                            'max_length': 255
                        },
                    'is_lazy': True
                },
                {
                    'setting': 'lazy_empty_setting',
                    'name': "Fish's name",
                    'field_extra': {
                            'min_length': 2,
                            'max_length': 255
                        },
                    'is_lazy': True
                },
            )
        }

        migrate_settings_group(apps, test_group)

        self.assertTrue(gateway.lazy_fish_name)
        self.assertTrue(db_settings.lazy_fish_name)

        self.assertTrue(gateway.lazy_fish_name)
        self.assertEqual(
            gateway.get_lazy_setting('lazy_fish_name'), 'Lazy Eric')
        self.assertTrue(db_settings.lazy_fish_name)
        self.assertEqual(
            db_settings.get_lazy_setting('lazy_fish_name'), 'Lazy Eric')

        self.assertTrue(gateway.lazy_empty_setting is None)
        self.assertTrue(db_settings.lazy_empty_setting is None)
        with self.assertRaises(ValueError):
            db_settings.get_lazy_setting('fish_name')
