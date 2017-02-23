from django.contrib.auth import get_user_model
from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.users.models import Ban
from misago.users.testutils import AuthenticatedUserTestCase


UserModel = get_user_model()


class UserProfileViewsTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(UserProfileViewsTests, self).setUp()
        self.link_kwargs = {'slug': self.user.slug, 'pk': self.user.pk}

        self.category = Category.objects.get(slug='first-category')

    def test_outdated_slugs(self):
        """user profile view redirects to valid slug"""
        response = self.client.get(
            reverse('misago:user-posts', kwargs={
                'slug': 'baww',
                'pk': self.user.pk,
            })
        )

        self.assertEqual(response.status_code, 301)

    def test_user_disabled(self):
        """disabled user's profile returns 404 for non-admins"""
        self.user.is_staff = False
        self.user.save()

        test_user = UserModel.objects.create_user('Tyrael', 't123@test.com', 'pass123')

        test_user.is_active = False
        test_user.save()

        response = self.client.get(test_user.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        self.user.is_staff = True
        self.user.save()

        response = self.client.get(test_user.get_absolute_url())
        self.assertEqual(response.status_code, 302)

        # profile page displays notice about user being disabled
        response = self.client.get(response['location'])
        self.assertContains(response, "account has been disabled", status_code=200)

    def test_user_posts_list(self):
        """user profile posts list has no showstoppers"""
        link = reverse('misago:user-posts', kwargs=self.link_kwargs)
        response = self.client.get(link)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have posted no messages")

        thread = testutils.post_thread(
            category=self.category,
            poster=self.user,
        )

        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, thread.get_absolute_url())

        post = testutils.reply_thread(thread, poster=self.user)
        other_post = testutils.reply_thread(thread, poster=self.user)

        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.get_absolute_url())
        self.assertContains(response, other_post.get_absolute_url())

    def test_user_threads_list(self):
        """user profile threads list has no showstoppers"""
        link = reverse('misago:user-threads', kwargs=self.link_kwargs)

        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have no started threads.")

        thread = testutils.post_thread(
            category=self.category,
            poster=self.user,
        )

        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, thread.get_absolute_url())

        post = testutils.reply_thread(thread, poster=self.user)
        other_post = testutils.reply_thread(thread, poster=self.user)

        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, post.get_absolute_url())
        self.assertNotContains(response, other_post.get_absolute_url())

    def test_user_followers(self):
        """user profile followers list has no showstoppers"""
        response = self.client.get(reverse(
            'misago:user-followers',
            kwargs=self.link_kwargs,
        ))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have no followers.')

        followers = []
        for i in range(10):
            user_data = ("Follower%s" % i, "foll%s@test.com" % i, "Pass.123")
            followers.append(UserModel.objects.create_user(*user_data))
            self.user.followed_by.add(followers[-1])

        response = self.client.get(reverse(
            'misago:user-followers',
            kwargs=self.link_kwargs,
        ))
        self.assertEqual(response.status_code, 200)
        for i in range(10):
            self.assertContains(response, "Follower%s" % i)

    def test_user_follows(self):
        """user profile follows list has no showstoppers"""
        response = self.client.get(reverse(
            'misago:user-follows',
            kwargs=self.link_kwargs,
        ))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are not following any users.')

        followers = []
        for i in range(10):
            user_data = ("Follower%s" % i, "foll%s@test.com" % i, "Pass.123")
            followers.append(UserModel.objects.create_user(*user_data))
            followers[-1].followed_by.add(self.user)

        response = self.client.get(reverse(
            'misago:user-follows',
            kwargs=self.link_kwargs,
        ))
        self.assertEqual(response.status_code, 200)
        for i in range(10):
            self.assertContains(response, "Follower%s" % i)

    def test_username_history_list(self):
        """user name changes history list has no showstoppers"""
        response = self.client.get(reverse(
            'misago:username-history',
            kwargs=self.link_kwargs,
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your username was never changed.')

        self.user.set_username('RenamedAdmin')
        self.user.save()
        self.user.set_username('TestUser')
        self.user.save()

        response = self.client.get(reverse(
            'misago:username-history',
            kwargs=self.link_kwargs,
        ))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestUser")
        self.assertContains(response, "RenamedAdmin")

    def test_user_ban_details(self):
        """user ban details page has no showstoppers"""
        override_acl(self.user, {
            'can_see_ban_details': 0,
        })

        test_user = UserModel.objects.create_user("Bob", "bob@bob.com", 'pass.123')
        link_kwargs = {'slug': test_user.slug, 'pk': test_user.pk}

        response = self.client.get(reverse(
            'misago:user-ban',
            kwargs=link_kwargs,
        ))
        self.assertEqual(response.status_code, 404)

        override_acl(self.user, {
            'can_see_ban_details': 1,
        })

        response = self.client.get(reverse(
            'misago:user-ban',
            kwargs=link_kwargs,
        ))
        self.assertEqual(response.status_code, 404)

        override_acl(self.user, {
            'can_see_ban_details': 1,
        })
        test_user.ban_cache.delete()

        Ban.objects.create(
            banned_value=test_user.username,
            user_message="User m3ss4ge.",
            staff_message="Staff m3ss4ge.",
            is_checked=True,
        )

        response = self.client.get(reverse(
            'misago:user-ban',
            kwargs=link_kwargs,
        ))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User m3ss4ge')
        self.assertContains(response, 'Staff m3ss4ge')
