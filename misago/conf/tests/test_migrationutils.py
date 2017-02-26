from django.apps import apps
from django.test import TestCase

from misago.conf import migrationutils
from misago.conf.models import SettingsGroup
from misago.core import threadstore


class DBConfMigrationUtilsTests(TestCase):
    def setUp(self):
        self.test_group = {
            'key': 'test_group',
            'name': "Test settings",
            'description': "Those are test settings.",
            'settings': [
                {
                    'setting': 'fish_name',
                    'name': "Fish's name",
                    'value': "Eric",
                    'field_extra': {
                        'min_length': 2,
                        'max_length': 255,
                    },
                },
                {
                    'setting': 'fish_license_no',
                    'name': "Fish's license number",
                    'default_value': '123-456',
                    'field_extra': {
                        'max_length': 255,
                    },
                },
            ],
        }

        migrationutils.migrate_settings_group(apps, self.test_group)
        self.groups_count = SettingsGroup.objects.count()

    def tearDown(self):
        threadstore.clear()

    def test_get_custom_group_and_settings(self):
        """tests setup created settings group"""
        custom_group = migrationutils.get_group(
            apps.get_model('misago_conf', 'SettingsGroup'), self.test_group['key']
        )

        self.assertEqual(custom_group.key, self.test_group['key'])
        self.assertEqual(custom_group.name, self.test_group['name'])
        self.assertEqual(custom_group.description, self.test_group['description'])

        custom_settings = migrationutils.get_custom_settings_values(custom_group)

        self.assertEqual(custom_settings['fish_name'], 'Eric')
        self.assertTrue('fish_license_no' not in custom_settings)

    def test_change_group_key(self):
        """migrate_settings_group changed group key"""

        new_group = {
            'key': 'new_test_group',
            'name': "New test settings",
            'description': "Those are updated test settings.",
            'settings': [
                {
                    'setting': 'fish_new_name',
                    'name': "Fish's new name",
                    'value': "Eric",
                    'field_extra': {
                        'min_length': 2,
                        'max_length': 255,
                    },
                },
                {
                    'setting': 'fish_new_license_no',
                    'name': "Fish's changed license number",
                    'default_value': '123-456',
                    'field_extra': {
                        'max_length': 255,
                    },
                },
            ],
        }

        migrationutils.migrate_settings_group(
            apps, new_group, old_group_key=self.test_group['key']
        )

        db_group = migrationutils.get_group(
            apps.get_model('misago_conf', 'SettingsGroup'), new_group['key']
        )

        self.assertEqual(SettingsGroup.objects.count(), self.groups_count)
        self.assertEqual(db_group.key, new_group['key'])
        self.assertEqual(db_group.name, new_group['name'])
        self.assertEqual(db_group.description, new_group['description'])

        for setting in new_group['settings']:
            db_setting = db_group.setting_set.get(setting=setting['setting'])
            self.assertEqual(db_setting.name, setting['name'])
