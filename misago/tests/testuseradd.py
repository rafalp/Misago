from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase
from misago.models import User, Rank, Role
from misago.monitor import Monitor

class UserAddTestCase(TestCase):
    def setUp(self):
        call_command('startmisago', quiet=True)

    def test_user_from_model(self):
        """Test User.objects.create_user"""

        user_a = User.objects.create_user('Lemmiwinks', 'lemm@sp.com', '123pass')

        monitor = Monitor()
        self.assertEqual(int(monitor['users']), 1)
        self.assertEqual(int(monitor['users_inactive']), 0)
        self.assertEqual(int(monitor['last_user']), user_a.pk)
        self.assertEqual(monitor['last_user_name'], user_a.username)
        self.assertEqual(monitor['last_user_slug'], user_a.username_slug)

        user_b = User.objects.create_user('InactiveTest', 'lemsm@sp.com', '123pass', activation=User.ACTIVATION_USER)

        monitor = Monitor()
        self.assertEqual(int(monitor['users']), 1)
        self.assertEqual(int(monitor['users_inactive']), 1)
        self.assertEqual(int(monitor['last_user']), user_a.pk)
        self.assertEqual(monitor['last_user_name'], user_a.username)
        self.assertEqual(monitor['last_user_slug'], user_a.username_slug)

        try:
            user_c = User.objects.create_user('UsedMail', 'lemsm@sp.com', '123pass')
            raise AssertionError("Created user account with taken e-mail address!")
        except ValidationError:
            pass

        monitor = Monitor()
        self.assertEqual(int(monitor['users']), 1)
        self.assertEqual(int(monitor['users_inactive']), 1)
        self.assertEqual(int(monitor['last_user']), user_a.pk)
        self.assertEqual(monitor['last_user_name'], user_a.username)
        self.assertEqual(monitor['last_user_slug'], user_a.username_slug)

        try:
            user_d = User.objects.create_user('InactiveTest', 'user@name.com', '123pass')
            raise AssertionError("Created user account with taken username!")
        except ValidationError:
            pass

        monitor = Monitor()
        self.assertEqual(int(monitor['users']), 1)
        self.assertEqual(int(monitor['users_inactive']), 1)
        self.assertEqual(int(monitor['last_user']), user_a.pk)
        self.assertEqual(monitor['last_user_name'], user_a.username)
        self.assertEqual(monitor['last_user_slug'], user_a.username_slug)