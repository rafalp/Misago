from django.urls import reverse

from ...acl.test import patch_user_acl
from ...categories.models import Category
from ...threads.test import post_thread
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


class ActivePostersTests(UsersListTestCase):
    def test_empty_active_posters_list(self):
        """empty active posters page has no showstoppers"""
        view_link = reverse("misago:users-active-posters")

        response = self.client.get(view_link)
        self.assertEqual(response.status_code, 200)

    def test_active_posters_list(self):
        """active posters page has no showstoppers"""
        category = Category.objects.get(slug="first-category")
        view_link = reverse("misago:users-active-posters")

        response = self.client.get(view_link)
        self.assertEqual(response.status_code, 200)

        # Create 50 test users and see if errors appeared
        for i in range(50):
            user = create_test_user("Bob%s" % i, "m%s@te.com" % i, posts=12345)
            post_thread(category, poster=user)

        build_active_posters_ranking()

        response = self.client.get(view_link)
        self.assertEqual(response.status_code, 200)


class UsersRankTests(UsersListTestCase):
    def test_ranks(self):
        """ranks lists are handled correctly"""
        rank_user = create_test_user("Visible", "visible@te.com")

        for rank in Rank.objects.iterator():
            rank_user.rank = rank
            rank_user.save()

            rank_link = reverse("misago:users-rank", kwargs={"slug": rank.slug})
            response = self.client.get(rank_link)

            if rank.is_tab:
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, rank_user.get_absolute_url())
            else:
                self.assertEqual(response.status_code, 404)

    def test_disabled_users(self):
        """ranks lists excludes disabled accounts"""
        rank_user = create_test_user("Visible", "visible@te.com", is_active=False)

        for rank in Rank.objects.iterator():
            rank_user.rank = rank
            rank_user.save()

            rank_link = reverse("misago:users-rank", kwargs={"slug": rank.slug})
            response = self.client.get(rank_link)

            if rank.is_tab:
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, rank_user.get_absolute_url())
            else:
                self.assertEqual(response.status_code, 404)

    def test_staff_see_disabled_users(self):
        """ranks lists shows disabled accounts for staff members"""
        self.user.is_staff = True
        self.user.save()

        rank_user = create_test_user("Visible", "visible@te.com", is_active=False)

        for rank in Rank.objects.iterator():
            rank_user.rank = rank
            rank_user.save()

            rank_link = reverse("misago:users-rank", kwargs={"slug": rank.slug})
            response = self.client.get(rank_link)

            if rank.is_tab:
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, rank_user.get_absolute_url())
            else:
                self.assertEqual(response.status_code, 404)
