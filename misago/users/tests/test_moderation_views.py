from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl

from misago.users.models import Ban
from misago.users.testutils import AuthenticatedUserTestCase


class UserModerationTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(UserModerationTestCase, self).setUp()
        self.test_user = get_user_model().objects.create_user(
            "Bob", "bob@bob.com", "Pass.123")
        self.link_kwargs = {'user_slug': 'bob', 'user_id': self.test_user.pk}


class RenameUserTests(UserModerationTestCase):
    def allow_rename(self):
        override_acl(self.user, {
            'can_rename_users': 1,
        })

    def test_no_rename_permission(self):
        """user with no permission fails to rename other user"""
        override_acl(self.user, {
            'can_rename_users': 0,
        })

        response = self.client.get(
            reverse('misago:rename_user', kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can&#39;t rename users.", response.content)

    def test_rename_user(self):
        """user with permission renames other user"""
        self.allow_rename()
        response = self.client.get(
            reverse('misago:rename_user', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)

        self.allow_rename()
        response = self.client.post(
            reverse('misago:rename_user', kwargs=self.link_kwargs),
            data={'new_username': 'LoremIpsum'})
        self.assertEqual(response.status_code, 302)

        self.allow_rename()
        response = self.client.post(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bob&#39;s username has been changed.', response.content)


class ModerateAvatarTests(UserModerationTestCase):
    def allow_avatar_mod(self):
        override_acl(self.user, {
            'can_moderate_avatars': 1,
        })

    def test_no_avatar_mod_permission(self):
        """user with no permission fails to mod other user avatar"""
        override_acl(self.user, {
            'can_moderate_avatars': 0,
        })

        response = self.client.get(
            reverse('misago:moderate_avatar', kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can&#39;t moderate avatars.", response.content)

    def test_mod_avatar(self):
        """user with permission moderates other user avatar"""
        self.allow_avatar_mod()
        response = self.client.get(
            reverse('misago:moderate_avatar', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)

        self.allow_avatar_mod()
        response = self.client.post(
            reverse('misago:moderate_avatar', kwargs=self.link_kwargs),
            data={
                'is_avatar_locked': '1',
                'avatar_lock_user_message': 'Test us3r message',
                'avatar_lock_staff_message': 'Test st4ff message'
            })
        self.assertEqual(response.status_code, 302)

        User = get_user_model()
        updated_user = User.objects.get(id=self.test_user.pk)

        self.assertTrue(updated_user.is_avatar_locked)
        self.assertEqual(updated_user.avatar_lock_user_message,
                         'Test us3r message')
        self.assertEqual(updated_user.avatar_lock_staff_message,
                         'Test st4ff message')

        self.allow_avatar_mod()
        response = self.client.get(
            reverse('misago:moderate_avatar', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test us3r message', response.content)
        self.assertIn('Test st4ff message', response.content)


class ModerateSignatureTests(UserModerationTestCase):
    def allow_signature_mod(self):
        override_acl(self.user, {
            'can_moderate_signatures': 1,
        })

    def test_no_signature_mod_permission(self):
        """user with no permission fails to mod other user signature"""
        override_acl(self.user, {
            'can_moderate_signatures': 0,
        })

        response = self.client.get(
            reverse('misago:moderate_signature', kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can&#39;t moderate signatures.", response.content)

    def test_mod_signature(self):
        """user with permission moderates other user signature"""
        self.allow_signature_mod()
        response = self.client.get(
            reverse('misago:moderate_signature', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)

        self.allow_signature_mod()
        response = self.client.post(
            reverse('misago:moderate_signature', kwargs=self.link_kwargs),
            data={
                'signature': 'kittens!',
                'is_signature_locked': '1',
                'signature_lock_user_message': 'Test us3r message',
                'signature_lock_staff_message': 'Test st4ff message'
            })
        self.assertEqual(response.status_code, 302)

        User = get_user_model()
        updated_user = User.objects.get(id=self.test_user.pk)

        self.assertTrue(updated_user.is_signature_locked)
        self.assertEqual(updated_user.signature_parsed, '<p>kittens!</p>')
        self.assertEqual(updated_user.signature_lock_user_message,
                         'Test us3r message')
        self.assertEqual(updated_user.signature_lock_staff_message,
                         'Test st4ff message')

        self.allow_signature_mod()
        response = self.client.get(
            reverse('misago:moderate_signature', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test us3r message', response.content)
        self.assertIn('Test st4ff message', response.content)


class BanUserTests(UserModerationTestCase):
    def allow_ban_user(self):
        override_acl(self.user, {
            'can_ban_users': 1,
            'max_ban_length': 0,
        })

    def test_no_ban_permission(self):
        """user with no permission fails to ban other user"""
        override_acl(self.user, {
            'can_ban_users': 0,
        })

        response = self.client.get(
            reverse('misago:ban_user', kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can&#39;t ban users.", response.content)

    def test_ban_user(self):
        """user with permission bans other user"""
        self.allow_ban_user()
        response = self.client.get(
            reverse('misago:ban_user', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)

        self.allow_ban_user()
        response = self.client.post(
            reverse('misago:ban_user', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 302)

        self.allow_ban_user()
        response = self.client.post(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bob has been banned.', response.content)

        Ban.objects.get(banned_value=self.test_user.username.lower())


class LiftUserBanTests(UserModerationTestCase):
    def allow_lift_ban(self):
        override_acl(self.user, {
            'can_lift_bans': 1,
            'max_lifted_ban_length': 0,
        })

    def test_no_lift_ban_permission(self):
        """user with no permission fails to lift user ban"""
        override_acl(self.user, {
            'can_lift_bans': 0,
            'max_lifted_ban_length': 0,
        })

        Ban.objects.create(banned_value=self.test_user.username)

        response = self.client.post(
            reverse('misago:lift_user_ban', kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can&#39;t lift bans.", response.content)

    def test_lift_user_ban(self):
        """user with permission lifts other user ban"""
        test_ban = Ban.objects.create(banned_value=self.test_user.username)

        self.allow_lift_ban()
        response = self.client.post(
            reverse('misago:lift_user_ban', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 302)

        self.allow_lift_ban()
        response = self.client.post(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('ban has been lifted.', response.content)

        test_ban = Ban.objects.get(id=test_ban.pk)
        self.assertTrue(test_ban.is_expired)


class DeleteUserTests(UserModerationTestCase):
    def test_no_delete_permission(self):
        """user with no permission fails to delete other user"""
        override_acl(self.user, {
            'can_delete_users_newer_than': 0,
            'can_delete_users_with_less_posts_than': 0,
        })

        response = self.client.post(
            reverse('misago:delete_user', kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can&#39;t delete users.", response.content)

    def test_delete_user(self):
        """user with permission deletes other user"""
        override_acl(self.user, {
            'can_delete_users_newer_than': 5,
            'can_delete_users_with_less_posts_than': 5,
        })

        response = self.client.post(
            reverse('misago:delete_user', kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bob has been deleted', response.content)
