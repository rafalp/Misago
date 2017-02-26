import json

from django.contrib.auth import get_user_model

from misago.acl.testutils import override_acl
from misago.conf import settings
from misago.users.testutils import AuthenticatedUserTestCase


UserModel = get_user_model()


class UserUsernameTests(AuthenticatedUserTestCase):
    """tests for user change name RPC (POST to /api/users/1/username/)"""

    def setUp(self):
        super(UserUsernameTests, self).setUp()
        self.link = '/api/users/%s/username/' % self.user.pk

    def test_get_change_username_options(self):
        """get to API returns options"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertIsNotNone(response_json['changes_left'])
        self.assertEqual(response_json['length_min'], settings.username_length_min)
        self.assertEqual(response_json['length_max'], settings.username_length_max)
        self.assertIsNone(response_json['next_on'])

        for i in range(response_json['changes_left']):
            self.user.set_username('NewName%s' % i, self.user)

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['changes_left'], 0)
        self.assertIsNotNone(response_json['next_on'])

    def test_change_username_no_changes_left(self):
        """api returns error 400 if there are no username changes left"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        for i in range(response_json['changes_left']):
            self.user.set_username('NewName%s' % i, self.user)

        response = self.client.get(self.link)
        response_json = response.json()
        self.assertEqual(response_json['changes_left'], 0)

        response = self.client.post(
            self.link,
            data={
                'username': 'Pointless',
            },
        )

        self.assertContains(response, 'change your username now', status_code=400)
        self.assertTrue(self.user.username != 'Pointless')

    def test_change_username_no_input(self):
        """api returns error 400 if new username is empty"""
        response = self.client.post(self.link, data={})

        self.assertContains(response, 'Enter new username.', status_code=400)

    def test_change_username_invalid_name(self):
        """api returns error 400 if new username is wrong"""
        response = self.client.post(
            self.link,
            data={
                'username': '####',
            },
        )

        self.assertContains(response, 'can only contain latin', status_code=400)

    def test_change_username(self):
        """api changes username and records change"""
        response = self.client.get(self.link)
        changes_left = response.json()['changes_left']

        old_username = self.user.username
        new_username = 'NewUsernamu'

        response = self.client.post(
            self.link,
            data={
                'username': new_username,
            },
        )

        self.assertEqual(response.status_code, 200)
        options = response.json()['options']
        self.assertEqual(changes_left, options['changes_left'] + 1)

        self.reload_user()
        self.assertEqual(self.user.username, new_username)
        self.assertTrue(self.user.username != old_username)

        self.assertEqual(self.user.namechanges.last().new_username, new_username)


class UserUsernameModerationTests(AuthenticatedUserTestCase):
    """tests for moderate username RPC (/api/users/1/moderate-username/)"""

    def setUp(self):
        super(UserUsernameModerationTests, self).setUp()

        self.other_user = UserModel.objects.create_user("OtherUser", "other@user.com", "pass123")

        self.link = '/api/users/%s/moderate-username/' % self.other_user.pk

    def test_no_permission(self):
        """no permission to moderate avatar"""
        override_acl(self.user, {
            'can_rename_users': 0,
        })

        response = self.client.get(self.link)
        self.assertContains(response, "can't rename users", status_code=403)

        override_acl(self.user, {
            'can_rename_users': 0,
        })

        response = self.client.post(self.link)
        self.assertContains(response, "can't rename users", status_code=403)

    def test_moderate_username(self):
        """moderate username"""
        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = response.json()
        self.assertEqual(options['length_min'], settings.username_length_min)
        self.assertEqual(options['length_max'], settings.username_length_max)

        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.post(
            self.link,
            json.dumps({
                'username': '',
            }),
            content_type='application/json',
        )

        self.assertContains(response, "Enter new username", status_code=400)

        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.post(
            self.link,
            json.dumps({
                'username': '$$$',
            }),
            content_type='application/json',
        )

        self.assertContains(
            response,
            "Username can only contain latin alphabet letters and digits.",
            status_code=400
        )

        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.post(
            self.link,
            json.dumps({
                'username': 'a',
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response, "Username must be at least 3 characters long.", status_code=400
        )

        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.post(
            self.link,
            json.dumps({
                'username': 'BobBoberson',
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)

        other_user = UserModel.objects.get(pk=self.other_user.pk)

        self.assertEqual('BobBoberson', other_user.username)
        self.assertEqual('bobboberson', other_user.slug)

        options = response.json()
        self.assertEqual(options['username'], other_user.username)
        self.assertEqual(options['slug'], other_user.slug)

    def test_moderate_own_username(self):
        """moderate own username"""
        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.get('/api/users/%s/moderate-username/' % self.user.pk)
        self.assertEqual(response.status_code, 200)
