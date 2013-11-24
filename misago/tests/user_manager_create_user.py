from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase
from misago.models import User
from misago.monitor import Monitor

class UserManagerCreateUserTestCase(TestCase):
    def setUp(self):
        call_command('startmisago', quiet=True)

    def test_create_user(self):
        """Test User.objects.create_user"""

        user_a = User.objects.create_user('Lemmiwinks', 'lemm@sp.com', '123pass')
        try:
            user_from_db = User.objects.get(username=user_a.username)
            user_from_db = User.objects.get(email=user_a.email)
        except User.DoesNotExist:
            raise AssertionError("User A was not saved in database!")

        monitor = Monitor()
        self.assertEqual(int(monitor['users']), 1)
        self.assertEqual(int(monitor['users_inactive']), 0)
        self.assertEqual(int(monitor['last_user']), user_a.pk)
        self.assertEqual(monitor['last_user_name'], user_a.username)
        self.assertEqual(monitor['last_user_slug'], user_a.username_slug)

        user_b = User.objects.create_user('InactiveTest', 'lemsm@sp.com', '123pass', activation=User.ACTIVATION_USER)
        try:
            user_from_db = User.objects.get(username=user_b.username)
            user_from_db = User.objects.get(email=user_b.email)
            self.assertEqual(user_from_db.activation, User.ACTIVATION_USER)
        except User.DoesNotExist:
            raise AssertionError("User B was not saved in database!")

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