from django.test import TestCase
from misago.conf.hydrators import hydrate_value, dehydrate_value


class HydratorsTests(TestCase):
    def test_hydrate_dehydrate_string(self):
        """string value is correctly hydrated and dehydrated"""
        wet_value = 'Ni!'
        dry_value = dehydrate_value('string', wet_value)
        self.assertEqual(hydrate_value('string', dry_value), wet_value)

    def test_hydrate_dehydrate_bool(self):
        """bool values is correctly hydrated and dehydrated"""
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
        """list value is correctly hydrated and dehydrated"""
        wet_value = ['foxtrot', 'uniform', 'hotel']
        dry_value = dehydrate_value('list', wet_value)
        self.assertEqual(hydrate_value('list', dry_value), wet_value)

    def test_hydrate_dehydrate_empty_list(self):
        """list value is correctly hydrated and dehydrated"""
        wet_value = []
        dry_value = dehydrate_value('list', wet_value)
        self.assertEqual(hydrate_value('list', dry_value), wet_value)
