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

    def test_user_followers(self):
        """user profile followers list has no showstoppers"""
        User = get_user_model()

        response = self.client.get(reverse('misago:user_followers',
                                           kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertIn('No users are following you', response.content)

        followers = []
        for i in xrange(10):
            user_data = ("Follower%s" % i, "foll%s@test.com" % i, "Pass.123")
            followers.append(User.objects.create_user(*user_data))
            self.test_admin.followed_by.add(followers[-1])

        response = self.client.get(reverse('misago:user_followers',
                                           kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)
        for i in xrange(10):
            self.assertIn("Follower%s" % i, response.content)

    def test_user_follows(self):
        """user profile follows list has no showstoppers"""
        User = get_user_model()

        response = self.client.get(reverse('misago:user_follows',
                                           kwargs=self.link_kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Your are not following any users', response.content)

        followers = []
        for i in xrange(10):
            user_data = ("Follower%s" % i, "foll%s@test.com" % i, "Pass.123")
            followers.append(User.objects.create_user(*user_data))
            followers[-1].followed_by.add(self.test_admin)

        response = self.client.get(reverse('misago:user_follows',
                                           kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)
        for i in xrange(10):
            self.assertIn("Follower%s" % i, response.content)

    def test_user_follow(self):
        """user profile follows list has no showstoppers"""
        User = get_user_model()
        test_user = User.objects.create_user(
            "Other", "other@test.com", "Pass.123")
        link_kwargs = {'user_slug': test_user.slug, 'user_id': test_user.pk}

        response = self.client.post(reverse('misago:follow_user',
                                            kwargs=link_kwargs))
        self.assertEqual(response.status_code, 302)

        test_admin = User.objects.get(id=self.test_admin.pk)
        self.assertEqual(test_admin.following, 1)

        test_user = User.objects.get(id=test_user.pk)
        self.assertEqual(test_user.followers, 1)

        self.assertIn(test_admin, test_user.followed_by.all())

        response = self.client.post(reverse('misago:follow_user',
                                            kwargs=link_kwargs))
        self.assertEqual(response.status_code, 302)

        test_admin = User.objects.get(id=self.test_admin.pk)
        self.assertEqual(test_admin.following, 0)

        test_user = User.objects.get(id=test_user.pk)
        self.assertEqual(test_user.followers, 0)

        self.assertNotIn(test_admin, test_user.followed_by.all())

    def test_user_block(self):
        """user profile follows list has no showstoppers"""
        User = get_user_model()
        test_user = User.objects.create_user(
            "Other", "other@test.com", "Pass.123")
        link_kwargs = {'user_slug': test_user.slug, 'user_id': test_user.pk}

        response = self.client.post(reverse('misago:block_user',
                                            kwargs=link_kwargs))
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.test_admin, test_user.blocked_by.all())

        response = self.client.post(reverse('misago:block_user',
                                            kwargs=link_kwargs))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.test_admin, test_user.blocked_by.all())

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
            'can_see_ban_details': 0,
        })

        User = get_user_model()
        test_user = User.objects.create_user("Bob", "bob@bob.com", 'pass.123')
        link_kwargs = {'user_slug': test_user.slug, 'user_id': test_user.pk}

        response = self.client.get(reverse('misago:user_ban',
                                           kwargs=link_kwargs))
        self.assertEqual(response.status_code, 404)

        override_acl(self.test_admin, {
            'can_see_ban_details': 1,
        })

        Ban.objects.create(banned_value=test_user.username,
                           user_message="User m3ss4ge.",
                           staff_message="Staff m3ss4ge.")

        response = self.client.get(reverse('misago:user_ban',
                                           kwargs=link_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertIn('User m3ss4ge', response.content)
        self.assertIn('Staff m3ss4ge', response.content)
