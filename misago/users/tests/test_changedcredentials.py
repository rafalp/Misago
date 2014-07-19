from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.users import changedcredentials


class ChangedCredentialsTests(TestCase):
    def test_credentials_change(self):
        """changedcredentials module allows for credentials change"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@bob.com', 'pass123')

        credentials_token = changedcredentials.cache_new_credentials(
            test_user, 'newbob@test.com', 'newpass123')

        new_credentials = changedcredentials.get_new_credentials(
            test_user, credentials_token)

        self.assertEqual(new_credentials['email'], 'newbob@test.com')
        self.assertEqual(new_credentials['password'], 'newpass123')
