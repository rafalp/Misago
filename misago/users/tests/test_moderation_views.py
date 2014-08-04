from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.admin.testutils import AdminTestCase

from misago.users.models import Ban


class UserModerationTestCase(AdminTestCase):
    def setUp(self):
        super(UserModerationTestCase, self).setUp()
        self.test_user = get_user_model().objects.create_user(
            "Bob", "bob@bob.com", "Pass.123")
        self.link_kwargs = {'user_slug': 'bob', 'user_id': self.test_user.pk}


class RenameUserTests(UserModerationTestCase):
    def test_no_rename_permission(self):
        """user with no permission fails to rename other user"""
        override_acl(self.test_admin, {
            'misago.users.permissions.moderation': {
                'can_rename_users': 0,
            },
        })

        response = self.client.get(
            reverse('misago:rename_user', kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can&#39;t rename users.", response.content)

    def test_rename_user(self):
        """user with permission renames other user"""
        override_acl(self.test_admin, {
            'misago.users.permissions.moderation': {
                'can_rename_users': 1,
            }
        })

        response = self.client.get(
            reverse('misago:rename_user', kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:rename_user', kwargs=self.link_kwargs),
            data={'new_username': 'LoremIpsum'})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bob&#39;s username has been changed.', response.content)


class ModerateAvatarTests(UserModerationTestCase):
    def test_no_rename_permission(self):
        """user with no permission fails to mod other user avatar"""
        override_acl(self.test_admin, {
            'misago.users.permissions.moderation': {
                'can_moderate_avatars': 0,
            },
        })

        response = self.client.get(
            reverse('misago:moderate_avatar', kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can&#39;t moderate avatars.", response.content)

    def test_rename_user(self):
        """user with permission moderates other user avatar"""
        override_acl(self.test_admin, {
            'misago.users.permissions.moderation': {
                'can_moderate_avatars': 1,
            }
        })

        response = self.client.get(
            reverse('misago:moderate_avatar', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:moderate_avatar', kwargs=self.link_kwargs),
            data={
                'is_avatar_banned': '1',
                'avatar_ban_user_message': 'Test us3r message',
                'avatar_ban_staff_message': 'Test st4ff message'
            })
        self.assertEqual(response.status_code, 302)

        User = get_user_model()
        updated_user = User.objects.get(id=self.test_user.pk)

        self.assertTrue(updated_user.is_avatar_banned)
        self.assertEqual(updated_user.avatar_ban_user_message,
                         'Test us3r message')
        self.assertEqual(updated_user.avatar_ban_staff_message,
                         'Test st4ff message')

        response = self.client.get(
            reverse('misago:moderate_avatar', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test us3r message', response.content)
        self.assertIn('Test st4ff message', response.content)


class ModerateSignatureTests(UserModerationTestCase):
    def test_no_rename_permission(self):
        """user with no permission fails to mod other user signature"""
        override_acl(self.test_admin, {
            'misago.users.permissions.moderation': {
                'can_moderate_signatures': 0,
            },
        })

        response = self.client.get(
            reverse('misago:moderate_signature', kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can&#39;t moderate signatures.", response.content)

    def test_rename_user(self):
        """user with permission moderates other user signature"""
        override_acl(self.test_admin, {
            'misago.users.permissions.moderation': {
                'can_moderate_signatures': 1,
            }
        })

        response = self.client.get(
            reverse('misago:moderate_signature', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:moderate_signature', kwargs=self.link_kwargs),
            data={
                'signature': 'kittens!',
                'is_signature_banned': '1',
                'signature_ban_user_message': 'Test us3r message',
                'signature_ban_staff_message': 'Test st4ff message'
            })
        self.assertEqual(response.status_code, 302)

        User = get_user_model()
        updated_user = User.objects.get(id=self.test_user.pk)

        self.assertTrue(updated_user.is_signature_banned)
        self.assertEqual(updated_user.signature_parsed, '<p>kittens!</p>')
        self.assertEqual(updated_user.signature_ban_user_message,
                         'Test us3r message')
        self.assertEqual(updated_user.signature_ban_staff_message,
                         'Test st4ff message')

        response = self.client.get(
            reverse('misago:moderate_signature', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test us3r message', response.content)
        self.assertIn('Test st4ff message', response.content)


class BanUserTests(UserModerationTestCase):
    def test_no_ban_permission(self):
        """user with no permission fails to ban other user"""
        override_acl(self.test_admin, {
            'misago.users.permissions.moderation': {
                'can_ban_users': 0,
            },
        })

        response = self.client.get(
            reverse('misago:ban_user', kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can&#39;t ban users.", response.content)

    def test_ban_user(self):
        """user with permission bans other user"""
        override_acl(self.test_admin, {
            'misago.users.permissions.moderation': {
                'can_ban_users': 1,
                'max_ban_length': 0,
            }
        })

        response = self.client.get(
            reverse('misago:ban_user', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:ban_user', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bob has been banned.', response.content)

        Ban.objects.get(banned_value=self.test_user.username.lower())


class LiftUserBanTests(UserModerationTestCase):
    def test_no_lift_ban_permission(self):
        """user with no permission fails to lift user ban"""
        override_acl(self.test_admin, {
            'misago.users.permissions.moderation': {
                'can_lift_bans': 0,
                'max_lifted_ban_length': 0,
            },
        })

        Ban.objects.create(banned_value=self.test_user.username)

        response = self.client.post(
            reverse('misago:lift_user_ban', kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can&#39;t lift bans.", response.content)

    def test_lift_user_ban(self):
        """user with permission lifts other user ban"""
        override_acl(self.test_admin, {
            'misago.users.permissions.moderation': {
                'can_lift_bans': 1,
                'max_lifted_ban_length': 0,
            }
        })

        test_ban = Ban.objects.create(banned_value=self.test_user.username)

        response = self.client.post(
            reverse('misago:lift_user_ban', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('ban has been lifted.', response.content)

        test_ban = Ban.objects.get(id=test_ban.pk)
        self.assertTrue(test_ban.is_expired)


class DeleteUserTests(UserModerationTestCase):
    def test_no_delete_permission(self):
        """user with no permission fails to delete other user"""
        override_acl(self.test_admin, {
            'misago.users.permissions.delete': {
                'can_delete_users_newer_than': 0,
                'can_delete_users_with_less_posts_than': 0,
            },
        })

        response = self.client.post(
            reverse('misago:delete_user', kwargs=self.link_kwargs))

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

        response = self.client.post(
            reverse('misago:delete_user', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bob has been deleted', response.content)
