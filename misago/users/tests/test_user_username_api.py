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


class UserUsernameModerationTests(AuthenticatedUserTestCase):
    """
    tests for moderate username RPC (/api/users/1/moderate-username/)
    """
    def setUp(self):
        super(UserUsernameModerationTests, self).setUp()

        User = get_user_model()
        self.other_user = User.objects.create_user(
            "OtherUser", "other@user.com", "pass123")

        self.link = '/api/users/%s/moderate-username/' % self.other_user.pk

    def test_no_permission(self):
        """no permission to moderate avatar"""
        override_acl(self.user, {
            'can_rename_users': 0,
        })

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertIn("can't rename users", response.content)

        override_acl(self.user, {
            'can_rename_users': 0,
        })

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertIn("can't rename users", response.content)

    def test_moderate_username(self):
        """moderate username"""
        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = json.loads(response.content)
        self.assertEqual(options['length_min'],
                         settings.username_length_min)
        self.assertEqual(options['length_max'],
                         settings.username_length_max)

        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.post(self.link, json.dumps({
                'username': '',
            }),
            content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("Enter new username", response.content)

        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.post(self.link, json.dumps({
                'username': '$$$',
            }),
            content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Username can only contain latin alphabet letters and digits.",
            response.content)

        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.post(self.link, json.dumps({
                'username': 'a',
            }),
            content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Username must be at least 3 characters long.", response.content)

        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.post(self.link, json.dumps({
                'username': 'BobBoberson',
            }),
            content_type="application/json")

        self.assertEqual(response.status_code, 200)

        User = get_user_model()
        other_user = User.objects.get(pk=self.other_user.pk)

        self.assertEqual('BobBoberson', other_user.username)
        self.assertEqual('bobboberson', other_user.slug)

        options = json.loads(response.content)
        self.assertEqual(options['username'], other_user.username)
        self.assertEqual(options['slug'], other_user.slug)

    def test_moderate_own_username(self):
        """moderate own username"""
        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.get(
            '/api/users/%s/moderate-username/' % self.user.pk)
        self.assertEqual(response.status_code, 200)
