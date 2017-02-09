from django.test import TestCase

from misago.conf.hydrators import dehydrate_value, hydrate_value
from misago.conf.models import Setting


class HydratorsTests(TestCase):
    def test_hydrate_dehydrate_string(self):
        """string value is correctly hydrated and dehydrated"""
        wet_value = 'Ni!'
        dry_value = dehydrate_value('string', wet_value)
        self.assertEqual(hydrate_value('string', dry_value), wet_value)

    def test_hydrate_dehydrate_bool(self):
        """bool values are correctly hydrated and dehydrated"""
        wet_value = True
        dry_value = dehydrate_value('bool', wet_value)
        self.assertEqual(hydrate_value('bool', dry_value), wet_value)

        wet_value = False
        dry_value = dehydrate_value('bool', wet_value)
        self.assertEqual(hydrate_value('bool', dry_value), wet_value)

    def test_hydrate_dehydrate_int(self):
        """int value is correctly hydrated and dehydrated"""
        wet_value = 9001
        dry_value = dehydrate_value('int', wet_value)
        self.assertEqual(hydrate_value('int', dry_value), wet_value)

    def test_hydrate_dehydrate_list(self):
        """list is correctly hydrated and dehydrated"""
        wet_value = ['foxtrot', 'uniform', 'hotel']
        dry_value = dehydrate_value('list', wet_value)
        self.assertEqual(hydrate_value('list', dry_value), wet_value)

    def test_hydrate_dehydrate_empty_list(self):
        """empty list is correctly hydrated and dehydrated"""
        wet_value = []
        dry_value = dehydrate_value('list', wet_value)
        self.assertEqual(hydrate_value('list', dry_value), wet_value)

    def test_value_error(self):
        """unsupported type raises ValueError"""
        with self.assertRaises(ValueError):
            hydrate_value('eric', None)

        with self.assertRaises(ValueError):
            dehydrate_value('eric', None)


class HydratorsModelTests(TestCase):
    def test_hydrate_dehydrate_string(self):
        """string value is correctly hydrated and dehydrated in model"""
        setting = Setting(python_type='string')

        wet_value = 'Lorem Ipsum'
        dry_value = dehydrate_value(setting.python_type, wet_value)

        setting.value = wet_value
        self.assertEqual(setting.value, wet_value)
        self.assertEqual(setting.dry_value, dry_value)

    def test_hydrate_dehydrate_bool(self):
        """bool values are correctly hydrated and dehydrated in model"""
        setting = Setting(python_type='bool')

        wet_value = True
        dry_value = dehydrate_value(setting.python_type, wet_value)

        setting.value = wet_value
        self.assertEqual(setting.value, wet_value)
        self.assertEqual(setting.dry_value, dry_value)

        wet_value = False
        dry_value = dehydrate_value(setting.python_type, wet_value)

        setting.value = wet_value
        self.assertEqual(setting.value, wet_value)
        self.assertEqual(setting.dry_value, dry_value)

    def test_hydrate_dehydrate_int(self):
        """int value is correctly hydrated and dehydrated in model"""
        setting = Setting(python_type='int')

        wet_value = 9001
        dry_value = dehydrate_value(setting.python_type, wet_value)

        setting.value = wet_value
        self.assertEqual(setting.value, wet_value)
        self.assertEqual(setting.dry_value, dry_value)

    def test_hydrate_dehydrate_list(self):
        """list is correctly hydrated and dehydrated in model"""
        setting = Setting(python_type='list')

        wet_value = ['Lorem', 'Ipsum', 'Dolor', 'Met']
        dry_value = dehydrate_value(setting.python_type, wet_value)

        setting.value = wet_value
        self.assertEqual(setting.value, wet_value)
        self.assertEqual(setting.dry_value, dry_value)

    def test_hydrate_dehydrate_empty_list(self):
        """empty list is correctly hydrated and dehydrated in model"""
        setting = Setting(python_type='list')

        wet_value = []
        dry_value = dehydrate_value(setting.python_type, wet_value)

        setting.value = wet_value
        self.assertEqual(setting.value, wet_value)
        self.assertEqual(setting.dry_value, dry_value)
