from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.core import threadstore
from misago.core.cache import cache

from misago.users import warnings
from misago.users.models import WarningLevel, UserWarning


class WarningsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.test_mod = User.objects.create_user('Modo', 'mod@mod.com',
                                                 'Pass.123')
        self.test_user = User.objects.create_user('Bob', 'bob@bob.com',
                                                  'Pass.123')

    def test_warnings(self):
        """user warning levels is obtained"""
        threadstore.clear()
        cache.clear()

        self.assertTrue(warnings.is_user_warning_level_max(self.test_user))

        levels = (
            WarningLevel.objects.create(name="Level 1"),
            WarningLevel.objects.create(name="Level 2"),
            WarningLevel.objects.create(name="Level 3"),
            WarningLevel.objects.create(name="Level 4"),
            WarningLevel.objects.create(name="Level 5"),
            WarningLevel.objects.create(name="Level 6"),
            WarningLevel.objects.create(name="Level 7"),
            WarningLevel.objects.create(name="Level 8")
        )

        self.assertEqual(WarningLevel.objects.count(), 8)

        threadstore.clear()
        cache.clear()

        for level, warning in enumerate(levels):
            warnings.warn_user(self.test_mod, self.test_user, "bawww")

            user_level = warnings.get_user_warning_level(self.test_user)
            user_level_obj = warnings.get_user_warning_obj(self.test_user)

            self.assertEqual(user_level, level + 1)
            self.assertEqual(user_level_obj.name, levels[level].name)
            self.assertEqual(self.test_user.warning_level, level + 1)

        self.assertTrue(warnings.is_user_warning_level_max(self.test_user))

        previous_level = user_level
        for warning in self.test_user.warnings.all():
            warnings.cancel_warning(self.test_mod, self.test_user, warning)
            user_level = warnings.get_user_warning_level(self.test_user)
            self.assertEqual(user_level + 1, previous_level)
            previous_level = user_level

        self.assertEqual(0, warnings.get_user_warning_level(self.test_user))


class WarningModelTests(TestCase):
    def test_warning_is_expired(self):
        """warning knows wheter or not its expired"""
        warning = UserWarning(given_on=timezone.now() - timedelta(days=6))
        self.assertTrue(warning.is_expired(60))
        self.assertFalse(warning.is_expired(14 * 24 * 3600))
