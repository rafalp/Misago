import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.encoding import smart_str

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.core import threadstore
from misago.core.cache import cache
from misago.threads.models import Post, Thread
from misago.threads.testutils import post_thread
from misago.users.activepostersranking import build_active_posters_ranking
from misago.users.models import Ban, Rank
from misago.users.testutils import AuthenticatedUserTestCase


UserModel = get_user_model()


class ActivePostersListTests(AuthenticatedUserTestCase):
    """tests for active posters list (GET /users/?list=active)"""

    def setUp(self):
        super(ActivePostersListTests, self).setUp()
        self.link = '/api/users/?list=active'

        cache.clear()
        threadstore.clear()

        self.category = Category.objects.all_categories()[:1][0]
        self.category.labels = []

    def test_empty_list(self):
        """empty list is served"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.user.username)

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.user.username)

    def test_filled_list(self):
        """filled list is served"""
        post_thread(self.category, poster=self.user)
        self.user.posts = 1
        self.user.save()

        build_active_posters_ranking()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, '"is_online":true')
        self.assertContains(response, '"is_offline":false')

        self.logout_user()
        build_active_posters_ranking()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, '"is_online":false')
        self.assertContains(response, '"is_offline":true')


class FollowersListTests(AuthenticatedUserTestCase):
    """tests for generic list (GET /users/) filtered by followers"""

    def setUp(self):
        super(FollowersListTests, self).setUp()
        self.link = '/api/users/%s/followers/'

    def test_nonexistent_user(self):
        """list for non-existing user returns 404"""
        response = self.client.get(self.link % 31242)
        self.assertEqual(response.status_code, 404)

    def test_empty_list(self):
        """user without followers returns 200"""
        response = self.client.get(self.link % self.user.pk)
        self.assertEqual(response.status_code, 200)

    def test_filled_list(self):
        """user with followers returns 200"""
        test_follower = UserModel.objects.create_user(
            "TestFollower",
            "test@follower.com",
            self.USER_PASSWORD,
        )
        self.user.followed_by.add(test_follower)

        response = self.client.get(self.link % self.user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_follower.username)

    def test_filled_list_search(self):
        """followers list is searchable"""
        test_follower = UserModel.objects.create_user(
            "TestFollower",
            "test@follower.com",
            self.USER_PASSWORD,
        )
        self.user.followed_by.add(test_follower)

        api_link = self.link % self.user.pk

        response = self.client.get('%s?search=%s' % (api_link, 'test'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_follower.username)


class FollowsListTests(AuthenticatedUserTestCase):
    """tests for generic list (GET /users/) filtered by follows"""

    def setUp(self):
        super(FollowsListTests, self).setUp()
        self.link = '/api/users/%s/follows/'

    def test_nonexistent_user(self):
        """list for non-existing user returns 404"""
        response = self.client.get(self.link % 1321)
        self.assertEqual(response.status_code, 404)

    def test_empty_list(self):
        """user without follows returns 200"""
        response = self.client.get(self.link % self.user.pk)
        self.assertEqual(response.status_code, 200)

    def test_filled_list(self):
        """user with follows returns 200"""
        test_follower = UserModel.objects.create_user(
            "TestFollower",
            "test@follower.com",
            self.USER_PASSWORD,
        )
        self.user.follows.add(test_follower)

        response = self.client.get(self.link % self.user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_follower.username)

    def test_filled_list_search(self):
        """follows list is searchable"""
        test_follower = UserModel.objects.create_user(
            "TestFollower",
            "test@follower.com",
            self.USER_PASSWORD,
        )
        self.user.follows.add(test_follower)

        api_link = self.link % self.user.pk

        response = self.client.get('%s?search=%s' % (api_link, 'test'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_follower.username)


class RankListTests(AuthenticatedUserTestCase):
    """tests for generic list (GET /users/) filtered by rank"""

    def setUp(self):
        super(RankListTests, self).setUp()
        self.link = '/api/users/?rank=%s'

    def test_nonexistent_rank(self):
        """list for non-existing rank returns 404"""
        response = self.client.get(self.link % 1421)
        self.assertEqual(response.status_code, 404)

    def test_empty_list(self):
        """tab rank without members returns 200"""
        test_rank = Rank.objects.create(
            name="Test rank",
            slug="test-rank",
            is_tab=True,
        )

        response = self.client.get(self.link % test_rank.pk)
        self.assertEqual(response.status_code, 200)

    def test_disabled_list(self):
        """non-tab rank returns 404"""
        self.user.rank.is_tab = False
        self.user.rank.save()

        response = self.client.get(self.link % self.user.rank.pk)
        self.assertEqual(response.status_code, 404)

    def test_list_search(self):
        """rank list is not searchable"""
        api_link = self.link % self.user.rank.pk

        response = self.client.get('%s&name=%s' % (api_link, 'test'))
        self.assertEqual(response.status_code, 404)

    def test_filled_list(self):
        """tab rank with members return 200"""
        self.user.rank.is_tab = True
        self.user.rank.save()

        response = self.client.get(self.link % self.user.rank.pk)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_disabled_users(self):
        """api follows disabled users visibility"""
        test_rank = Rank.objects.create(
            name="Test rank",
            slug="test-rank",
            is_tab=True,
        )

        test_user = UserModel.objects.create_user(
            'Visible',
            'visible@te.com',
            'Pass.123',
            rank=test_rank,
            is_active=False,
        )

        response = self.client.get(self.link % test_rank.pk)
        self.assertNotContains(response, test_user.get_absolute_url())

        # api shows disabled accounts to staff
        self.user.is_staff = True
        self.user.save()

        response = self.client.get(self.link % test_rank.pk)
        self.assertContains(response, test_user.get_absolute_url())


class SearchNamesListTests(AuthenticatedUserTestCase):
    """tests for generic list (GET /users/) filtered by username disallowing searches"""

    def setUp(self):
        super(SearchNamesListTests, self).setUp()
        self.link = '/api/users/?&name='

    def test_empty_list(self):
        """empty list returns 404"""
        response = self.client.get(self.link + 'this-user-is-fake')
        self.assertEqual(response.status_code, 404)

    def test_filled_list(self):
        """results list returns 404"""
        response = self.client.get(self.link + self.user.slug)
        self.assertEqual(response.status_code, 404)


class UserRetrieveTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(UserRetrieveTests, self).setUp()

        self.test_user = UserModel.objects.create_user('Tyrael', 't123@test.com', 'pass123')
        self.link = reverse(
            'misago:api:user-detail', kwargs={
                'pk': self.test_user.pk,
            }
        )

    def test_get_user(self):
        """api user retrieve endpoint has no showstoppers"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

    def test_disabled_user(self):
        """api user retrieve handles disabled users"""
        self.user.is_staff = False
        self.user.save()

        self.test_user.is_active = False
        self.test_user.save()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 404)

        self.user.is_staff = True
        self.user.save()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)


class UserForumOptionsTests(AuthenticatedUserTestCase):
    """tests for user forum options RPC (POST to /api/users/1/forum-options/)"""

    def setUp(self):
        super(UserForumOptionsTests, self).setUp()
        self.link = '/api/users/%s/forum-options/' % self.user.pk

    def test_empty_request(self):
        """empty request is handled"""
        response = self.client.post(self.link)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'limits_private_thread_invites_to': [
                    'This field is required.',
                ],
                'subscribe_to_started_threads': [
                    'This field is required.',
                ],
                'subscribe_to_replied_threads': [
                    'This field is required.',
                ],
            }
        )

    def test_change_forum_invalid_ranges(self):
        """api validates ranges for fields"""
        response = self.client.post(
            self.link,
            data={
                'limits_private_thread_invites_to': 541,
                'subscribe_to_started_threads': 44,
                'subscribe_to_replied_threads': 321,
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'limits_private_thread_invites_to': [
                    '"541" is not a valid choice.',
                ],
                'subscribe_to_started_threads': [
                    '"44" is not a valid choice.',
                ],
                'subscribe_to_replied_threads': [
                    '"321" is not a valid choice.',
                ],
            }
        )

    def test_change_forum_options(self):
        """forum options are changed"""
        response = self.client.post(
            self.link,
            data={
                'limits_private_thread_invites_to': 1,
                'subscribe_to_started_threads': 2,
                'subscribe_to_replied_threads': 1,
            }
        )
        self.assertEqual(response.status_code, 200)

        self.reload_user()

        self.assertFalse(self.user.is_hiding_presence)
        self.assertEqual(self.user.limits_private_thread_invites_to, 1)
        self.assertEqual(self.user.subscribe_to_started_threads, 2)
        self.assertEqual(self.user.subscribe_to_replied_threads, 1)

        response = self.client.post(
            self.link,
            data={
                'is_hiding_presence': True,
                'limits_private_thread_invites_to': 1,
                'subscribe_to_started_threads': 2,
                'subscribe_to_replied_threads': 1,
            }
        )
        self.assertEqual(response.status_code, 200)

        self.reload_user()

        self.assertTrue(self.user.is_hiding_presence)
        self.assertEqual(self.user.limits_private_thread_invites_to, 1)
        self.assertEqual(self.user.subscribe_to_started_threads, 2)
        self.assertEqual(self.user.subscribe_to_replied_threads, 1)

        response = self.client.post(
            self.link,
            data={
                'is_hiding_presence': False,
                'limits_private_thread_invites_to': 1,
                'subscribe_to_started_threads': 2,
                'subscribe_to_replied_threads': 1,
            }
        )
        self.assertEqual(response.status_code, 200)

        self.reload_user()

        self.assertFalse(self.user.is_hiding_presence)
        self.assertEqual(self.user.limits_private_thread_invites_to, 1)
        self.assertEqual(self.user.subscribe_to_started_threads, 2)
        self.assertEqual(self.user.subscribe_to_replied_threads, 1)


class UserFollowTests(AuthenticatedUserTestCase):
    """tests for user follow RPC (POST to /api/users/1/follow/)"""

    def setUp(self):
        super(UserFollowTests, self).setUp()

        self.other_user = UserModel.objects.create_user("OtherUser", "other@user.com", "pass123")

        self.link = '/api/users/%s/follow/' % self.other_user.pk

    def test_follow_unauthenticated(self):
        """you have to sign in to follow users"""
        self.logout_user()

        response = self.client.post(self.link)
        self.assertContains(response, "action is not available to guests", status_code=403)

    def test_follow_myself(self):
        """you can't follow yourself"""
        response = self.client.post('/api/users/%s/follow/' % self.user.pk)
        self.assertContains(response, "can't add yourself to followed", status_code=403)

    def test_cant_follow(self):
        """no permission to follow users"""
        override_acl(self.user, {
            'can_follow_users': 0,
        })

        response = self.client.post(self.link)
        self.assertContains(response, "can't follow other users", status_code=403)

    def test_follow(self):
        """follow and unfollow other user"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 200)

        user = UserModel.objects.get(pk=self.user.pk)
        self.assertEqual(user.followers, 0)
        self.assertEqual(user.following, 1)
        self.assertEqual(user.follows.count(), 1)
        self.assertEqual(user.followed_by.count(), 0)

        followed = UserModel.objects.get(pk=self.other_user.pk)
        self.assertEqual(followed.followers, 1)
        self.assertEqual(followed.following, 0)
        self.assertEqual(followed.follows.count(), 0)
        self.assertEqual(followed.followed_by.count(), 1)

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 200)

        user = UserModel.objects.get(pk=self.user.pk)
        self.assertEqual(user.followers, 0)
        self.assertEqual(user.following, 0)
        self.assertEqual(user.follows.count(), 0)
        self.assertEqual(user.followed_by.count(), 0)

        followed = UserModel.objects.get(pk=self.other_user.pk)
        self.assertEqual(followed.followers, 0)
        self.assertEqual(followed.following, 0)
        self.assertEqual(followed.follows.count(), 0)
        self.assertEqual(followed.followed_by.count(), 0)


class UserBanTests(AuthenticatedUserTestCase):
    """tests for ban endpoint (GET to /api/users/1/ban/)"""

    def setUp(self):
        super(UserBanTests, self).setUp()

        self.other_user = UserModel.objects.create_user("OtherUser", "other@user.com", "pass123")

        self.link = '/api/users/%s/ban/' % self.other_user.pk

    def test_no_permission(self):
        """user has no permission to access ban"""
        override_acl(self.user, {'can_see_ban_details': 0})

        response = self.client.get(self.link)
        self.assertContains(response, "can't see users bans details", status_code=403)

    def test_no_ban(self):
        """api returns empty json"""
        override_acl(self.user, {'can_see_ban_details': 1})

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(smart_str(response.content), '{}')

    def test_ban_details(self):
        """api returns ban json"""
        override_acl(self.user, {'can_see_ban_details': 1})

        Ban.objects.create(
            check_type=Ban.USERNAME,
            banned_value=self.other_user.username,
            user_message='Nope!',
        )

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        ban_json = response.json()
        self.assertEqual(ban_json['user_message']['plain'], 'Nope!')
        self.assertEqual(ban_json['user_message']['html'], '<p>Nope!</p>')


class UserDeleteTests(AuthenticatedUserTestCase):
    """tests for user delete RPC (POST to /api/users/1/delete/)"""

    def setUp(self):
        super(UserDeleteTests, self).setUp()

        self.other_user = UserModel.objects.create_user("OtherUser", "other@user.com", "pass123")

        self.link = '/api/users/%s/delete/' % self.other_user.pk

        self.threads = Thread.objects.count()
        self.posts = Post.objects.count()

        self.category = Category.objects.all_categories()[:1][0]

        post_thread(self.category, poster=self.other_user)
        self.other_user.posts = 1
        self.other_user.threads = 1
        self.other_user.save()

    def test_delete_no_permission(self):
        """raises 403 error when no permission to delete"""
        override_acl(
            self.user, {
                'can_delete_users_newer_than': 0,
                'can_delete_users_with_less_posts_than': 0,
            }
        )

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "can't delete users", status_code=403)

    def test_delete_too_many_posts(self):
        """raises 403 error when user has too many posts"""
        override_acl(
            self.user, {
                'can_delete_users_newer_than': 0,
                'can_delete_users_with_less_posts_than': 5,
            }
        )

        self.other_user.posts = 6
        self.other_user.save()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "can't delete users", status_code=403)
        self.assertContains(response, "made more than 5 posts", status_code=403)

    def test_delete_too_old_member(self):
        """raises 403 error when user is too old"""
        override_acl(
            self.user, {
                'can_delete_users_newer_than': 5,
                'can_delete_users_with_less_posts_than': 0,
            }
        )

        self.other_user.joined_on -= timedelta(days=6)
        self.other_user.save()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "can't delete users", status_code=403)
        self.assertContains(response, "members for more than 5 days", status_code=403)

    def test_delete_self(self):
        """raises 403 error when attempting to delete oneself"""
        override_acl(
            self.user, {
                'can_delete_users_newer_than': 10,
                'can_delete_users_with_less_posts_than': 10,
            }
        )

        response = self.client.post('/api/users/%s/delete/' % self.user.pk)
        self.assertContains(response, "can't delete yourself", status_code=403)

    def test_delete_admin(self):
        """raises 403 error when attempting to delete admin"""
        override_acl(
            self.user, {
                'can_delete_users_newer_than': 10,
                'can_delete_users_with_less_posts_than': 10,
            }
        )

        self.other_user.is_staff = True
        self.other_user.save()

        response = self.client.post(self.link)
        self.assertContains(response, "can't delete administrators", status_code=403)

    def test_delete_superadmin(self):
        """raises 403 error when attempting to delete superadmin"""
        override_acl(
            self.user, {
                'can_delete_users_newer_than': 10,
                'can_delete_users_with_less_posts_than': 10,
            }
        )

        self.other_user.is_superuser = True
        self.other_user.save()

        response = self.client.post(self.link)
        self.assertContains(response, "can't delete administrators", status_code=403)

    def test_delete_with_content(self):
        """returns 200 and deletes user with content"""
        override_acl(
            self.user, {
                'can_delete_users_newer_than': 10,
                'can_delete_users_with_less_posts_than': 10,
            }
        )

        response = self.client.post(
            self.link,
            json.dumps({
                'with_content': True
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(pk=self.other_user.pk)

        self.assertEqual(Thread.objects.count(), self.threads)
        self.assertEqual(Post.objects.count(), self.posts)

    def test_delete_without_content(self):
        """returns 200 and deletes user without content"""
        override_acl(
            self.user, {
                'can_delete_users_newer_than': 10,
                'can_delete_users_with_less_posts_than': 10,
            }
        )

        response = self.client.post(
            self.link,
            json.dumps({
                'with_content': False
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(pk=self.other_user.pk)

        self.assertEqual(Thread.objects.count(), self.threads + 1)
        self.assertEqual(Post.objects.count(), self.posts + 2)
