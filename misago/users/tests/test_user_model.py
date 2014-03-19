from django.test import TestCase
from misago.users.models import User


class UserModelTests(TestCase):
    def test_set_username(self):
        """set_username sets username and slug on model"""
        user = User()

        user.set_username('Boberson')
        self.assertEqual(user.username, 'Boberson')
        self.assertEqual(user.username_slug, 'boberson')

        self.assertEqual(user.get_username(), 'Boberson')
        self.assertEqual(user.get_full_name(), 'Boberson')
        self.assertEqual(user.get_short_name(), 'Boberson')

    def test_set_email(self):
        """set_email sets email and hash on model"""
        user = User()

        user.set_email('bOb@TEst.com')
        self.assertEqual(user.email, 'bOb@test.com')
        self.assertTrue(user.email_hash)
