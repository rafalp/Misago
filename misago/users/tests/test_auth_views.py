from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.users.models import Ban, BAN_USERNAME


class LoginViewTests(TestCase):
    def test_view_get_returns_200(self):
        """login view returns 200 on GET"""
        response = self.client.get(reverse('misago:login'))
        self.assertEqual(response.status_code, 200)

    def test_view_invalid_credentials(self):
        """login view returns 200 on invalid POST"""
        response = self.client.post(
            reverse('misago:login'),
            data={'username': 'nope', 'password': 'nope'})

        self.assertEqual(response.status_code, 200)
        self.assertIn("Your login or password is incorrect.", response.content)

    def test_view_signin(self):
        """login view signs user in"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        response = self.client.post(
            reverse('misago:login'),
            data={'username': 'Bob', 'password': 'Pass.123'})

        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bob', response.content)

    def test_view_signin_banned(self):
        """login view fails to sign banned user in"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        Ban.objects.create(test=BAN_USERNAME, banned_value='bob',
                           user_message='Nope!')

        response = self.client.post(
            reverse('misago:login'),
            data={'username': 'Bob', 'password': 'Pass.123'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('Nope!', response.content)

        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Bob', response.content)

    def test_view_signin_inactive(self):
        """login view fails to sign inactive user in"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123',
                                 requires_activation=1)

        response = self.client.post(
            reverse('misago:login'),
            data={'username': 'Bob', 'password': 'Pass.123'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('activate', response.content)

        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Bob', response.content)
