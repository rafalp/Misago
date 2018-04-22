from misago.acl.testutils import override_acl
from misago.core.utils import serialize_datetime
from misago.users.testutils import AuthenticatedUserTestCase


class UsernameChangesApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(UsernameChangesApiTests, self).setUp()
        self.link = '/api/username-changes/'

    def test_user_can_always_see_his_name_changes(self):
        """list returns own username changes"""
        self.user.set_username('NewUsername', self.user)
        self.user.save()

        override_acl(self.user, {'can_see_users_name_history': False})

        response = self.client.get('%s?user=%s' % (self.link, self.user.pk))
        self.assertEqual(response.status_code, 200)
        
        username_change = self.user.namechanges.all()[0]
        self.assertEqual(response.json(), {
            'page': 1,
            'pages': 1,
            'count': 1,
            'first': None,
            'previous': None,
            'next': None,
            'last': None,
            'before': 0,
            'more': 0,
            'results': [
                {
                    'id': username_change.id,
                    'user': {
                        'id': self.user.id,
                        'username': 'NewUsername',
                        'slug': 'newusername',
                        'avatars': self.user.avatars,
                    },
                    'changed_by': {
                        'id': self.user.id,
                        'username': 'NewUsername',
                        'slug': 'newusername',
                        'avatars': self.user.avatars,
                    },
                    'changed_by_username': 'NewUsername',
                    'changed_on': serialize_datetime(username_change.changed_on),
                    'new_username': 'NewUsername',
                    'old_username': 'TestUser'
                }
            ],
        })

    def test_list_handles_invalid_filter(self):
        """list raises 404 for invalid filter"""
        self.user.set_username('NewUsername', self.user)

        override_acl(self.user, {'can_see_users_name_history': True})

        response = self.client.get('%s?user=abcd' % self.link)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'NOT FOUND'})

    def test_list_handles_nonexisting_user(self):
        """list raises 404 for invalid user id"""
        self.user.set_username('NewUsername', self.user)

        override_acl(self.user, {'can_see_users_name_history': True})

        response = self.client.get('%s?user=142141' % self.link)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'NOT FOUND'})

    def test_list_handles_search(self):
        """list returns found username changes"""
        self.user.set_username('NewUsername', self.user)
        self.user.save()

        override_acl(self.user, {'can_see_users_name_history': False})

        response = self.client.get('%s?user=%s&search=new' % (self.link, self.user.pk))
        self.assertEqual(response.status_code, 200)
        
        username_change = self.user.namechanges.all()[0]
        self.assertEqual(response.json(), {
            'page': 1,
            'pages': 1,
            'count': 1,
            'first': None,
            'previous': None,
            'next': None,
            'last': None,
            'before': 0,
            'more': 0,
            'results': [
                {
                    'id': username_change.id,
                    'user': {
                        'id': self.user.id,
                        'username': 'NewUsername',
                        'slug': 'newusername',
                        'avatars': self.user.avatars,
                    },
                    'changed_by': {
                        'id': self.user.id,
                        'username': 'NewUsername',
                        'slug': 'newusername',
                        'avatars': self.user.avatars,
                    },
                    'changed_by_username': 'NewUsername',
                    'changed_on': serialize_datetime(username_change.changed_on),
                    'new_username': 'NewUsername',
                    'old_username': 'TestUser'
                }
            ],
        })

        override_acl(self.user, {'can_see_users_name_history': False})

        response = self.client.get('%s?user=%s&search=usernew' % (self.link, self.user.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'page': 1,
            'pages': 1,
            'count': 0,
            'first': None,
            'previous': None,
            'next': None,
            'last': None,
            'before': 0,
            'more': 0,
            'results': [],
        })

    def test_list_denies_permission(self):
        """list denies permission for other user (or all) if no access"""
        override_acl(self.user, {'can_see_users_name_history': False})

        response = self.client.get('%s?user=%s' % (self.link, self.user.pk + 1))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You don't have permission to see other users name history.",
        })

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You don't have permission to see other users name history.",
        })
