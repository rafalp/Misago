from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.admin.testutils import AdminTestCase


class UserModerationTestCase(AdminTestCase):
    def setUp(self):
        super(UserModerationTestCase, self).setUp()
        self.test_user = get_user_model().objects.create_user(
            "Bob", "bob@bob.com", "Pass.123")


class DeleteUserTests(UserModerationTestCase):
    def test_no_delete_permission(self):
        """user with no permission fails to delete other user"""
        override_acl(self.test_admin, {
            'misago.users.permissions.delete': {
                'can_delete_users_newer_than': 0,
                'can_delete_users_with_less_posts_than': 0,
            },
        })

        response = self.client.post(reverse('misago:delete_user', kwargs={
                                                'user_id': self.test_user.pk
                                            }))

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can&#39;t delete users.", response.content)

    def test_delete_user(self):
        """user with permission deletes other user"""
        override_acl(self.test_admin, {
            'misago.users.permissions.delete': {
                'can_delete_users_newer_than': 5,
                'can_delete_users_with_less_posts_than': 5,
            }
        })

        response = self.client.post(reverse('misago:delete_user', kwargs={
                                                'user_id': self.test_user.pk
                                            }))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bob has been deleted', response.content)
