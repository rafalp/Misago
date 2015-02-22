import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.users.models import Ban, BAN_USERNAME


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

        response = self.client.get(reverse('misago:api:auth_user'))
        self.assertEqual(response.status_code, 200)

        user_json = json.loads(response.content)
        self.assertEqual(user_json['id'], user.id)
        self.assertEqual(user_json['username'], user.username)

    def test_api_signin_banned(self):
        """login api fails to sign banned user in"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        ban = Ban.objects.create(check_type=BAN_USERNAME,
                                 banned_value='bob',
                                 user_message='You are tragically banned.')

        response = self.client.post(
            reverse('misago:api:login'),
            data={'username': 'Bob', 'password': 'Pass.123'})
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['code'], 'banned')
        self.assertEqual(response_json['detail']['message']['plain'],
                         ban.user_message)
        self.assertEqual(response_json['detail']['message']['html'],
                         '<p>%s</p>' % ban.user_message)

    def test_api_signin_inactive_admin(self):
        """login api fails to sign admin-activated user in"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123',
                                 requires_activation=1)

        response = self.client.post(
            reverse('misago:api:login'),
            data={'username': 'Bob', 'password': 'Pass.123'})
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['code'], 'inactive_user')

    def test_api_signin_inactive_user(self):
        """login api fails to sign user-activated user in"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123',
                                 requires_activation=2)

        response = self.client.post(
            reverse('misago:api:login'),
            data={'username': 'Bob', 'password': 'Pass.123'})
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['code'], 'inactive_admin')
