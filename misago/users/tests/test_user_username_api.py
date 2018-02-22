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

    def test_get_change_username_form_options(self):
        """get to API returns form options"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'changes_left': self.user.acl_cache['name_changes_allowed'],
            'next_change_on': None,
            'length_min': settings.username_length_min,
            'length_max': settings.username_length_max,
        })

        for i in range(response.json()['changes_left']):
            self.user.set_username('NewName%s' % i, self.user)

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['changes_left'], 0)
        self.assertIsNotNone(response.json()['next_change_on'])

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
                'username': 'FailedChanges',
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ["You can't change your username at this time."],
            'next_change_on': response.json()['next_change_on'],
        })
        
        self.reload_user()
        self.assertTrue(self.user.username != 'FailedChanges')

    def test_change_username_no_input(self):
        """api returns error 400 if new username is omitted or empty"""
        response = self.client.post(self.link, data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ["This field is required."],
        })

        response = self.client.post(self.link, data={'username': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ["This field may not be blank."],
        })

    def test_change_username_invalid_name(self):
        """api returns error 400 if new username is wrong"""
        response = self.client.post(
            self.link,
            data={
                'username': '####',
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ["Username can only contain latin alphabet letters and digits."],
        })

    def test_change_username(self):
        """api changes username and records change"""
        old_username = self.user.username
        new_username = 'NewUsernamu'

        response = self.client.post(
            self.link,
            data={
                'username': new_username,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'username': 'NewUsernamu',
            'slug': 'newusernamu',
            'changes_left': 1,
            'next_change_on': None,
        })

        self.reload_user()
        self.assertEqual(self.user.username, new_username)
        self.assertNotEqual(self.user.username, old_username)

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
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't rename users."
        })

        override_acl(self.user, {
            'can_rename_users': 0,
        })

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't rename users."
        })

    def test_invalid_username(self):
        """moderate username api validates username"""
        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.post(
            self.link,
            json.dumps({
                'username': None,
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ["This field may not be null."],
        })

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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ["This field may not be blank."],
        })

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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ["Username can only contain latin alphabet letters and digits."],
        })

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
        self.assertEqual(response.json(), {
            'username': ["Username must be at least 3 characters long."],
        })

    def test_get_username_requirements(self):
        """get to API returns username requirements"""
        override_acl(self.user, {
            'can_rename_users': 1,
        })

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'length_min': settings.username_length_min,
            'length_max': settings.username_length_max,
        })

    def test_moderate_username(self):
        """moderate username"""
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
