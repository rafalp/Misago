import json
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from ...acl.test import patch_user_acl
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...threads.models import Post, Thread
from ...threads.test import post_thread
from ..activepostersranking import build_active_posters_ranking
from ..models import Ban, DeletedUser, Rank
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


def test_users_api_rank_filter_returns_404_for_not_existing_rank(client, db):
    response = client.get("/api/users/?rank=404")
    assert response.status_code == 404


def test_users_api_rank_filter_returns_404_if_rank_tab_is_disabled(client, db):
    rank = Rank.objects.create(name="Test rank", slug="test-rank", is_tab=False)

    response = client.get(f"/api/users/?rank={rank.id}")
    assert response.status_code == 404


def test_users_api_rank_filter_returns_empty_list(client, other_user):
    rank = Rank.objects.create(name="Test rank", slug="test-rank", is_tab=True)

    response = client.get(f"/api/users/?rank={rank.id}")
    assert json.loads(response.content)["results"] == []


def test_users_api_rank_filter_returns_list_with_rank_user(client, other_user):
    rank = Rank.objects.create(name="Test rank", slug="test-rank", is_tab=True)

    other_user.rank = rank
    other_user.save()

    response = client.get(f"/api/users/?rank={rank.id}")
    assert json.loads(response.content)["results"][0]["id"] == other_user.id


def test_users_api_rank_filter_returns_excluded_deactivated_users(
    client, inactive_user
):
    rank = Rank.objects.create(name="Test rank", slug="test-rank", is_tab=True)

    inactive_user.rank = rank
    inactive_user.save()

    response = client.get(f"/api/users/?rank={rank.id}")
    assert json.loads(response.content)["results"] == []


def test_users_api_rank_filter_returns_deactivated_users_for_admin(
    admin_client, inactive_user
):
    rank = Rank.objects.create(name="Test rank", slug="test-rank", is_tab=True)

    inactive_user.rank = rank
    inactive_user.save()

    response = admin_client.get(f"/api/users/?rank={rank.id}")
    assert json.loads(response.content)["results"][0]["id"] == inactive_user.id


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


def test_user_api_returns_404_for_nonexisting_user(client, db):
    response = client.get(reverse("misago:api:user-detail", kwargs={"pk": 404}))
    assert response.status_code == 404


def test_user_api_returns_user_data(client, user):
    response = client.get(reverse("misago:api:user-detail", kwargs={"pk": user.id}))
    assert response.status_code == 200
    assert json.loads(response.content)["id"] == user.id


def test_user_api_returns_404_for_deactivated_user(client, inactive_user):
    response = client.get(
        reverse("misago:api:user-detail", kwargs={"pk": inactive_user.id})
    )
    assert response.status_code == 404


def test_user_api_returns_deactivated_user_data_for_admins(admin_client, inactive_user):
    response = admin_client.get(
        reverse("misago:api:user-detail", kwargs={"pk": inactive_user.id})
    )
    assert json.loads(response.content)["id"] == inactive_user.id


class UserFollowTests(AuthenticatedUserTestCase):
    """tests for user follow RPC (POST to /api/users/1/follow/)"""

    def setUp(self):
        super().setUp()

        self.other_user = create_test_user("Other_User", "otheruser@example.com")
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

        self.other_user = create_test_user("Other_User", "otheruser@example.com")
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


def test_user_delete_api_prevents_deletion_if_user_no_permission(
    user_client, other_user
):
    response = user_client.post(f"/api/users/{other_user.id}/delete/")
    assert response.status_code == 403
    assert json.loads(response.content) == {"detail": "You can't delete users."}


@patch_user_acl(
    {"can_delete_users_newer_than": 5, "can_delete_users_with_less_posts_than": 0}
)
def test_user_delete_api_prevents_deletion_if_user_is_too_old(user_client, other_user):
    other_user.joined_on -= timedelta(days=6)
    other_user.save()

    response = user_client.post(f"/api/users/{other_user.id}/delete/")
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "detail": "You can't delete users that are members for more than 5 days.",
    }


@patch_user_acl(
    {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 5}
)
def test_user_delete_api_prevents_deletion_if_user_has_too_many_posts(
    user_client, other_user
):
    other_user.posts = 6
    other_user.save()

    response = user_client.post(f"/api/users/{other_user.id}/delete/")
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "detail": "You can't delete users that made more than 5 posts.",
    }


@patch_user_acl(
    {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 5}
)
def test_user_delete_api_prevents_deletion_if_user_is_staff(user_client, staffuser):
    response = user_client.post(f"/api/users/{staffuser.id}/delete/")
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "detail": "Django staff users can't be deleted.",
    }


@patch_user_acl(
    {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 5}
)
def test_user_delete_api_prevents_deletion_if_user_is_admin(user_client, admin):
    response = user_client.post(f"/api/users/{admin.id}/delete/")
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "detail": "Administrators can't be deleted.",
    }


@patch_user_acl(
    {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 5}
)
def test_user_delete_api_prevents_deletion_if_user_is_root_admin(
    user_client, root_admin
):
    response = user_client.post(f"/api/users/{root_admin.id}/delete/")
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "detail": "Administrators can't be deleted.",
    }


@patch_user_acl(
    {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 5}
)
def test_user_delete_api_prevents_deletion_if_user_is_self(user_client, user):
    response = user_client.post(f"/api/users/{user.id}/delete/")
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "detail": "You can't delete your account.",
    }


@patch_user_acl(
    {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 5}
)
def test_user_delete_api_deletes_user_with_content(
    user_client, default_category, other_user
):
    thread = post_thread(default_category, poster=other_user)

    response = user_client.post(
        f"/api/users/{other_user.id}/delete/",
        json={"with_content": True},
    )
    assert response.status_code == 200

    with pytest.raises(User.DoesNotExist):
        other_user.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()


@patch_user_acl(
    {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 5}
)
def test_user_delete_api_deletes_user_without_content(
    user_client, default_category, other_user
):
    thread = post_thread(default_category, poster=other_user)

    response = user_client.post(
        f"/api/users/{other_user.id}/delete/",
        json={"with_content": False},
    )
    assert response.status_code == 200

    with pytest.raises(User.DoesNotExist):
        other_user.refresh_from_db()

    thread.refresh_from_db()


@patch_user_acl(
    {"can_delete_users_newer_than": 10, "can_delete_users_with_less_posts_than": 10}
)
def test_user_delete_api_creates_deleted_user_entry(user_client, other_user):
    response = user_client.post(f"/api/users/{other_user.id}/delete/")
    assert response.status_code == 200

    DeletedUser.objects.get(deleted_by=DeletedUser.DELETED_BY_STAFF)
