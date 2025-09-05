from django.urls import reverse

from ...acl.test import patch_user_acl
from ...test import assert_contains, assert_not_contains
from ..activepostersranking import build_active_posters_ranking
from ..models import Rank
from ..test import AuthenticatedUserTestCase, create_test_user


class UsersListTestCase(AuthenticatedUserTestCase):
    pass


class UsersListLanderTests(UsersListTestCase):
    @patch_user_acl({"can_browse_users_list": 0})
    def test_lander_no_permission(self):
        """lander returns 403 if user has no permission"""
        response = self.client.get(reverse("misago:users"))
        self.assertEqual(response.status_code, 403)

    def test_lander_redirect(self):
        """lander returns redirect to valid page if user has permission"""
        response = self.client.get(reverse("misago:users"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response["location"].endswith(reverse("misago:users-active-posters"))
        )


def test_active_posters_view_renders_empty(db, client):
    response = client.get(reverse("misago:users-active-posters"))
    assert response.status_code == 200


def test_active_posters_view_renders_with_items(
    client, thread_factory, default_category
):
    for i in range(10):
        user = create_test_user(f"User{i}", f"m{i}@example.com", posts=12345)
        thread_factory(default_category, starter=user)

    assert build_active_posters_ranking()

    response = client.get(reverse("misago:users-active-posters"))
    for i in range(10):
        assert_contains(response, f"User{i}")


def test_rank_users_list_is_not_available_if_rank_is_not_tab(client, other_user):
    rank = Rank.objects.create(name="Test Rank", is_tab=False)

    other_user.rank = rank
    other_user.save()

    response = client.get(reverse("misago:users-rank", kwargs={"slug": rank.slug}))
    assert response.status_code == 404


def test_rank_users_list_displays_rank_users_if_rank_is_tab(client, other_user):
    rank = Rank.objects.create(name="Test Rank", is_tab=True)

    other_user.rank = rank
    other_user.save()

    response = client.get(reverse("misago:users-rank", kwargs={"slug": rank.slug}))
    assert_contains(response, other_user.get_absolute_url())


def test_rank_users_list_excludes_deactivated_users(client, inactive_user):
    rank = Rank.objects.create(name="Test Rank", is_tab=True)

    inactive_user.rank = rank
    inactive_user.save()

    response = client.get(reverse("misago:users-rank", kwargs={"slug": rank.slug}))
    assert_not_contains(response, inactive_user.get_absolute_url())


def test_rank_users_list_displays_deactivated_users_for_admin(
    admin_client, inactive_user
):
    rank = Rank.objects.create(name="Test Rank", is_tab=True)

    inactive_user.rank = rank
    inactive_user.save()

    response = admin_client.get(
        reverse("misago:users-rank", kwargs={"slug": rank.slug})
    )
    assert_contains(response, inactive_user.get_absolute_url())
