import json

from django.contrib.auth import get_user_model

from misago.acl.testutils import override_acl
from misago.conf import settings

from misago.users.testutils import AuthenticatedUserTestCase


class UserUsernameTests(AuthenticatedUserTestCase):
    """
    tests for user change name RPC (POST to /api/users/1/username/)
    """
    def setUp(self):
        super(UserUsernameTests, self).setUp()
        self.link = '/api/users/%s/username/' % self.user.pk

    def test_get_change_username_options(self):
        """get to API returns options"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)

        self.assertIsNotNone(response_json['changes_left'])
        self.assertEqual(response_json['length_min'],
                         settings.username_length_min)
        self.assertEqual(response_json['length_max'],
                         settings.username_length_max)
        self.assertIsNone(response_json['next_on'])

        for i in xrange(response_json['changes_left']):
            self.user.set_username('NewName%s' % i, self.user)

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['changes_left'], 0)
        self.assertIsNotNone(response_json['next_on'])

    def test_change_username_no_changes_left(self):
        """api returns error 400 if there are no username changes left"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        for i in xrange(response_json['changes_left']):
            self.user.set_username('NewName%s' % i, self.user)

        response = self.client.get(self.link)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['changes_left'], 0)

        response = self.client.post(self.link, data={
            'username': 'Pointless'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('change your username now', response.content)
        self.assertTrue(self.user.username != 'Pointless')

    def test_change_username_no_input(self):
        """api returns error 400 if new username is empty"""
        response = self.client.post(self.link, data={})

        self.assertEqual(response.status_code, 400)
        self.assertIn('Enter new username.', response.content)

    def test_change_username_invalid_name(self):
        """api returns error 400 if new username is wrong"""
        response = self.client.post(self.link, data={
            'username': '####'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('can only contain latin', response.content)

    def test_change_username(self):
        """api changes username and records change"""
        response = self.client.get(self.link)
        changes_left = json.loads(response.content)['changes_left']

        username = self.user.username
        new_username = 'NewUsernamu'

        response = self.client.post(self.link, data={
            'username': new_username
        })

        self.assertEqual(response.status_code, 200)
        options = json.loads(response.content)['options']
        self.assertEqual(changes_left, options['changes_left'] + 1)

        self.reload_user()
        self.assertEqual(self.user.username, new_username)

        self.assertEqual(self.user.namechanges.last().new_username,
                         new_username)
