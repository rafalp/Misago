import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase


class AuthenticateAPITests(TestCase):
    def test_api_invalid_credentials(self):
        """login api returns 400 on invalid POST"""
        response = self.client.post(
            reverse('misago:api:login'),
            data={'username': 'nope', 'password': 'nope'})

        self.assertEqual(response.status_code, 400)
        self.assertIn("Login or password is incorrect.", response.content)

        response = self.client.get(reverse('misago:api:auth_user'))
        self.assertEqual(response.status_code, 200)

        user_json = json.loads(response.content)
        self.assertIsNone(user_json['id'])

    def test_api_signin(self):
        """api signs user in"""
        User = get_user_model()
        user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        response = self.client.post(
            reverse('misago:api:login'),
            data={'username': 'Bob', 'password': 'Pass.123'})

        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('misago:api:auth_user'))
        self.assertEqual(response.status_code, 200)

        user_json = json.loads(response.content)
        self.assertEqual(user_json['id'], user.id)
        self.assertEqual(user_json['username'], user.username)

    def test_api_signin_banned(self):
        """login api fails to sign banned user in"""
        raise NotImplemented("TODO: test_api_signin_banned")

    def test_api_signin_inactive(self):
        """login api fails to sign inactive user in"""
        raise NotImplemented("TODO: test_api_signin_inactive")
