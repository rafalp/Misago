import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse

from ...acl.test import patch_user_acl
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...threads.models import Post, Thread
from ...threads.test import post_thread
from ..activepostersranking import build_active_posters_ranking
from ..models import Ban, Rank
from ..test import AuthenticatedUserTestCase, create_test_user

User = get_user_model()


class ActivePostersListTests(AuthenticatedUserTestCase):
    """tests for active posters list (GET /users/?list=active)"""

    def setUp(self):
        super().setUp()

        self.link = "/api/users/?list=active"

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
        super().setUp()
        self.link = "/api/users/%s/followers/"

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
        follower = create_test_user("TestFollower", "test@follower.com")
        self.user.followed_by.add(follower)

        response = self.client.get(self.link % self.user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, follower.username)

    def test_filled_list_search(self):
        """followers list is searchable"""
        follower = create_test_user("TestFollower", "test@follower.com")
        self.user.followed_by.add(follower)

        api_link = self.link % self.user.pk

        response = self.client.get("%s?search=%s" % (api_link, "test"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, follower.username)


class FollowsListTests(AuthenticatedUserTestCase):
    """tests for generic list (GET /users/) filtered by follows"""

    def setUp(self):
        super().setUp()
        self.link = "/api/users/%s/follows/"

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
        follower = create_test_user("TestFollower", "test@follower.com")
        self.user.follows.add(follower)

        response = self.client.get(self.link % self.user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, follower.username)

    def test_filled_list_search(self):
        """follows list is searchable"""
        follower = create_test_user("TestFollower", "test@follower.com")
        self.user.follows.add(follower)

        api_link = self.link % self.user.pk

        response = self.client.get("%s?search=%s" % (api_link, "test"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, follower.username)


class RankListTests(AuthenticatedUserTestCase):
    """tests for generic list (GET /users/) filtered by rank"""

    def setUp(self):
        super().setUp()
        self.link = "/api/users/?rank=%s"

    def test_nonexistent_rank(self):
        """list for non-existing rank returns 404"""
        response = self.client.get(self.link % 1421)
        self.assertEqual(response.status_code, 404)

    def test_empty_list(self):
        """tab rank without members returns 200"""
        test_rank = Rank.objects.create(name="Test rank", slug="test-rank", is_tab=True)

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

        response = self.client.get("%s&name=%s" % (api_link, "test"))
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
        rank = Rank.objects.create(name="Test rank", slug="test-rank", is_tab=True)
        user = create_test_user(
            "DisabledUser", "disabled@example.com", rank=rank, is_active=False
        )

        response = self.client.get(self.link % rank.pk)
        self.assertNotContains(response, user.get_absolute_url())

        # api shows disabled accounts to staff
        self.user.is_staff = True
        self.user.save()

        response = self.client.get(self.link % rank.pk)
        self.assertContains(response, user.get_absolute_url())


class SearchNamesListTests(AuthenticatedUserTestCase):
    """tests for generic list (GET /users/) filtered by username disallowing searches"""

    def setUp(self):
        super().setUp()
        self.link = "/api/users/?&name="

    def test_empty_list(self):
        """empty list returns 404"""
        response = self.client.get(self.link + "this-user-is-fake")
        self.assertEqual(response.status_code, 404)

    def test_filled_list(self):
        """results list returns 404"""
        response = self.client.get(self.link + self.user.slug)
        self.assertEqual(response.status_code, 404)


class UserRetrieveTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.other_user = create_test_user("OtherUser", "otheruser@example.com")
        self.link = reverse("misago:api:user-detail", kwargs={"pk": self.other_user.pk})

    def test_get_user(self):
        """api user retrieve endpoint has no showstoppers"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

    def test_disabled_user(self):
        """api user retrieve handles disabled users"""
        self.user.is_staff = False
        self.user.save()

        self.other_user.is_active = False
        self.other_user.save()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 404)

        self.user.is_staff = True
        self.user.save()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)


class UserForumOptionsTests(AuthenticatedUserTestCase):
    """tests for user forum options RPC (POST to /api/users/1/forum-options/)"""

    def setUp(self):
        super().setUp()
        self.link = "/api/users/%s/forum-options/" % self.user.pk

    def test_empty_request(self):
        """empty request is handled"""
        response = self.client.post(self.link)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "limits_private_thread_invites_to": ["This field is required."],
                "subscribe_to_started_threads": ["This field is required."],
                "subscribe_to_replied_threads": ["This field is required."],
            },
        )

    def test_change_forum_invalid_ranges(self):
        """api validates ranges for fields"""
        response = self.client.post(
            self.link,
            data={
                "limits_private_thread_invites_to": 541,
                "subscribe_to_started_threads": 44,
                "subscribe_to_replied_threads": 321,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "limits_private_thread_invites_to": ['"541" is not a valid choice.'],
                "subscribe_to_started_threads": ['"44" is not a valid choice.'],
                "subscribe_to_replied_threads": ['"321" is not a valid choice.'],
            },
        )

    def test_change_forum_options(self):
        """forum options are changed"""
        response = self.client.post(
            self.link,
            data={
                "limits_private_thread_invites_to": 1,
                "subscribe_to_started_threads": 2,
                "subscribe_to_replied_threads": 1,
            },
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
                "is_hiding_presence": True,
                "limits_private_thread_invites_to": 1,
                "subscribe_to_started_threads": 2,
                "subscribe_to_replied_threads": 1,
            },
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
                "is_hiding_presence": False,
                "limits_private_thread_invites_to": 1,
                "subscribe_to_started_threads": 2,
                "subscribe_to_replied_threads": 1,
            },
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
        super().setUp()

        self.other_user = create_test_user("OtherUser", "otheruser@example.com")
        self.link = "/api/users/%s/follow/" % self.other_user.pk

    def test_follow_unauthenticated(self):
        """you have to sign in to follow users"""
        self.logout_user()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

    def test_follow_myself(self):
        """you can't follow yourself"""
        response = self.client.post("/api/users/%s/follow/" % self.user.pk)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't add yourself to followed."}
        )

    @patch_user_acl({"can_follow_users": 0})
    def test_cant_follow(self):
        """no permission to follow users"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't follow other users."})

    def test_follow(self):
        """follow and unfollow other user"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.followers, 0)
        self.assertEqual(self.user.following, 1)
        self.assertEqual(self.user.follows.count(), 1)
        self.assertEqual(self.user.followed_by.count(), 0)

        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.followers, 1)
        self.assertEqual(self.other_user.following, 0)
        self.assertEqual(self.other_user.follows.count(), 0)
        self.assertEqual(self.other_user.followed_by.count(), 1)

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.followers, 0)
        self.assertEqual(self.user.following, 0)
        self.assertEqual(self.user.follows.count(), 0)
        self.assertEqual(self.user.followed_by.count(), 0)

        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.followers, 0)
        self.assertEqual(self.other_user.following, 0)
        self.assertEqual(self.other_user.follows.count(), 0)
        self.assertEqual(self.other_user.followed_by.count(), 0)


class UserBanTests(AuthenticatedUserTestCase):
    """tests for ban endpoint (GET to /api/users/1/ban/)"""

    def setUp(self):
        super().setUp()

        self.other_user = create_test_user("OtherUser", "otheruser@example.com")
        self.link = "/api/users/%s/ban/" % self.other_user.pk

    @patch_user_acl({"can_see_ban_details": 0})
    def test_no_permission(self):
        """user has no permission to access ban"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't see users bans details."}
        )

    @patch_user_acl({"can_see_ban_details": 1})
    def test_no_ban(self):
        """api returns empty json"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    @patch_user_acl({"can_see_ban_details": 1})
    def test_ban_details(self):
        """api returns ban json"""
        Ban.objects.create(
            check_type=Ban.USERNAME,
            banned_value=self.other_user.username,
            user_message="Nope!",
        )

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        ban_json = response.json()
        self.assertEqual(ban_json["user_message"]["plain"], "Nope!")
        self.assertEqual(ban_json["user_message"]["html"], "<p>Nope!</p>")


class UserDeleteOwnAccountTests(AuthenticatedUserTestCase):
    """
    tests for user request own account delete RPC
    (POST to /api/users/1/delete-own-account/)
    """

    def setUp(self):
        super().setUp()
        self.api_link = "/api/users/%s/delete-own-account/" % self.user.pk

    @override_dynamic_settings(allow_delete_own_account=False)
    def test_delete_own_account_feature_disabled(self):
        """
        raises 403 error when attempting to delete own account but feature is disabled
        """
        response = self.client.post(self.api_link, {"password": self.USER_PASSWORD})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't delete your account."})

        self.reload_user()
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_deleting_account)

    @override_dynamic_settings(allow_delete_own_account=True)
    def test_delete_own_account_is_staff(self):
        """raises 403 error when attempting to delete own account as admin"""
        self.user.is_staff = True
        self.user.save()

        response = self.client.post(self.api_link, {"password": self.USER_PASSWORD})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "You can't delete your account because you are an administrator."
                )
            },
        )

        self.reload_user()
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_deleting_account)

    @override_dynamic_settings(allow_delete_own_account=True)
    def test_delete_own_account_is_superuser(self):
        """raises 403 error when attempting to delete own account as superadmin"""
        self.user.is_superuser = True
        self.user.save()

        response = self.client.post(self.api_link, {"password": self.USER_PASSWORD})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "You can't delete your account because you are an administrator."
                )
            },
        )

        self.reload_user()
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_deleting_account)

    @override_dynamic_settings(allow_delete_own_account=True)
    def test_delete_own_account_invalid_password(self):
        """
        raises 400 error when attempting to delete own account with invalid password
        """
        response = self.client.post(self.api_link, {"password": "hello"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"password": ["Entered password is invalid."]}
        )

        self.reload_user()
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_deleting_account)

    @override_dynamic_settings(allow_delete_own_account=True)
    def test_delete_own_account(self):
        """deactivates account and marks it for deletion"""
        response = self.client.post(self.api_link, {"password": self.USER_PASSWORD})
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertFalse(self.user.is_active)
        self.assertTrue(self.user.is_deleting_account)


class UserDeleteTests(AuthenticatedUserTestCase):
    """tests for user delete RPC (POST to /api/users/1/delete/)"""

    def setUp(self):
        super().setUp()

        self.other_user = create_test_user("OtherUser", "otheruser@example.com")
        self.link = "/api/users/%s/delete/" % self.other_user.pk

        self.threads = Thread.objects.count()
        self.posts = Post.objects.count()

        self.category = Category.objects.all_categories()[:1][0]

        post_thread(self.category, poster=self.other_user)
        self.other_user.posts = 1
        self.other_user.threads = 1
        self.other_user.save()

    @patch_user_acl(
        {"can_delete_users_newer_than": 0, "can_delete_users_with_less_posts_than": 0}
    )
    def test_delete_no_permission(self):
        """raises 403 error when no permission to delete"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't delete users."})

    @patch_user_acl(
        {"can_delete_users_newer_than": 0, "can_delete_users_with_less_posts_than": 5}
    )
    def test_delete_too_many_posts(self):
        """raises 403 error when user has too many posts"""
        self.other_user.posts = 6
        self.other_user.save()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't delete users that made more than 5 posts."},
        )

    @patch_user_acl(
        {"can_delete_users_newer_than": 5, "can_delete_users_with_less_posts_than": 0}
    )
    def test_delete_too_old_member(self):
        """raises 403 error when user is too old"""
        self.other_user.joined_on -= timedelta(days=6)
        self.other_user.save()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't delete users that are members for more than 5 days."},
        )

    @patch_user_acl(
        {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 10}
    )
    def test_delete_self(self):
        """raises 403 error when attempting to delete oneself"""
        response = self.client.post("/api/users/%s/delete/" % self.user.pk)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't delete your account."})

    @patch_user_acl(
        {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 10}
    )
    def test_delete_admin(self):
        """raises 403 error when attempting to delete admin"""
        self.other_user.is_staff = True
        self.other_user.save()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't delete administrators."}
        )

    @patch_user_acl(
        {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 10}
    )
    def test_delete_superadmin(self):
        """raises 403 error when attempting to delete superadmin"""
        self.other_user.is_superuser = True
        self.other_user.save()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't delete administrators."}
        )

    @patch_user_acl(
        {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 10}
    )
    def test_delete_with_content(self):
        """returns 200 and deletes user with content"""
        response = self.client.post(
            self.link,
            json.dumps({"with_content": True}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(User.DoesNotExist):
            self.other_user.refresh_from_db()

        self.assertEqual(Thread.objects.count(), self.threads)
        self.assertEqual(Post.objects.count(), self.posts)

    @patch_user_acl(
        {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 10}
    )
    def test_delete_without_content(self):
        """returns 200 and deletes user without content"""
        response = self.client.post(
            self.link,
            json.dumps({"with_content": False}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(User.DoesNotExist):
            self.other_user.refresh_from_db()

        self.assertEqual(Thread.objects.count(), self.threads + 1)
        self.assertEqual(Post.objects.count(), self.posts + 2)
