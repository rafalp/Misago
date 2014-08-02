from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.admin.testutils import AdminTestCase

from misago.users.models import Ban


class UserProfileViewsTests(AdminTestCase):
    def setUp(self):
        super(UserProfileViewsTests, self).setUp()
        self.link_kwargs = {
            'user_slug': self.test_admin.slug,
            'user_id': self.test_admin.pk
        }

    def test_outdated_slugs(self):
        """user profile view redirects to valid slig"""
        invalid_kwargs = {'user_slug': 'baww', 'user_id': self.test_admin.pk}
        response = self.client.get(reverse('misago:user_posts',
                                           kwargs=invalid_kwargs))

        self.assertEqual(response.status_code, 301)

    def test_user_posts_list(self):
        """user profile posts list has no showstoppers"""
        response = self.client.get(reverse('misago:user_posts',
                                           kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertIn('posted no messages', response.content)

    def test_user_threads_list(self):
        """user profile threads list has no showstoppers"""
        response = self.client.get(reverse('misago:user_threads',
                                           kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertIn('started no threads', response.content)

    def test_user_name_history_list(self):
        """user name changes history list has no showstoppers"""
        response = self.client.get(reverse('misago:user_name_history',
                                           kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Your username was never changed', response.content)

        self.test_admin.set_username('RenamedAdmin')
        self.test_admin.save()
        self.test_admin.set_username('TestAdmin')
        self.test_admin.save()

        response = self.client.get(reverse('misago:user_name_history',
                                           kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertIn("TestAdmin</strong> changed name to <strong>Renamed",
                      response.content)

    def test_user_ban(self):
        """user ban details page has no showstoppers"""
        override_acl(self.test_admin, {
            'misago.users.permissions.profiles': {
                'can_see_ban_details': 0,
            },
        })

        User = get_user_model()
        test_user = User.objects.create_user("Bob", "bob@bob.com", 'pass.123')
        link_kwargs = {'user_slug': test_user.slug, 'user_id': test_user.pk}

        response = self.client.get(reverse('misago:user_ban',
                                           kwargs=link_kwargs))
        self.assertEqual(response.status_code, 404)

        override_acl(self.test_admin, {
            'misago.users.permissions.profiles': {
                'can_see_ban_details': 1,
            },
        })

        test_ban = Ban.objects.create(banned_value=test_user.username,
                                      user_message="User m3ss4ge.",
                                      staff_message="Staff m3ss4ge.")

        response = self.client.get(reverse('misago:user_ban',
                                           kwargs=link_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertIn('User m3ss4ge', response.content)
        self.assertIn('Staff m3ss4ge', response.content)
