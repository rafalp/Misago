from misago.acl.testutils import override_acl
from misago.users.testutils import AuthenticatedUserTestCase


class UsernameChangesApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(UsernameChangesApiTests, self).setUp()
        self.link = '/api/username-changes/'

    def test_user_can_always_see_his_name_changes(self):
        """list returns own username changes"""
        self.user.set_username('NewUsername', self.user)

        override_acl(self.user, {'can_see_users_name_history': False})

        response = self.client.get('%s?user=%s' % (self.link, self.user.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_list_handles_invalid_filter(self):
        """list raises 404 for invalid filter"""
        self.user.set_username('NewUsername', self.user)

        override_acl(self.user, {'can_see_users_name_history': True})

        response = self.client.get('%s?user=abcd' % self.link)
        self.assertEqual(response.status_code, 404)

    def test_list_handles_nonexisting_user(self):
        """list raises 404 for invalid user id"""
        self.user.set_username('NewUsername', self.user)

        override_acl(self.user, {'can_see_users_name_history': True})

        response = self.client.get('%s?user=142141' % self.link)
        self.assertEqual(response.status_code, 404)

    def test_list_handles_search(self):
        """list returns found username changes"""
        self.user.set_username('NewUsername', self.user)

        override_acl(self.user, {'can_see_users_name_history': False})

        response = self.client.get('%s?user=%s&search=new' % (self.link, self.user.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

        response = self.client.get('%s?user=%s&search=usernew' % (self.link, self.user.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '[]')

    def test_list_denies_permission(self):
        """list denies permission for other user (or all) if no access"""
        override_acl(self.user, {'can_see_users_name_history': False})

        response = self.client.get('%s?user=%s' % (self.link, self.user.pk + 1))
        self.assertContains(response, "don't have permission to", status_code=403)

        response = self.client.get(self.link)
        self.assertContains(response, "don't have permission to", status_code=403)
