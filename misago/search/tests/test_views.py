from django.urls import reverse

from ...acl.test import patch_user_acl
from ...threads.search import SearchThreads
from ...users.test import AuthenticatedUserTestCase


class LandingTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.test_link = reverse("misago:search")

    @patch_user_acl({"can_search": False})
    def test_no_permission(self):
        """view validates permission to search forum"""
        response = self.client.get(self.test_link)
        self.assertContains(response, "have permission to search site", status_code=403)

    @patch_user_acl({"can_search": True})
    def test_redirect_to_provider(self):
        """view validates permission to search forum"""
        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 302)
        self.assertIn(SearchThreads.url, response["location"])


class SearchTests(AuthenticatedUserTestCase):
    @patch_user_acl({"can_search": False})
    def test_no_permission(self):
        """view validates permission to search forum"""
        response = self.client.get(
            reverse("misago:search", kwargs={"search_provider": "users"})
        )

        self.assertContains(response, "have permission to search site", status_code=403)

    def test_not_found(self):
        """view raises 404 for not found provider"""
        response = self.client.get(
            reverse("misago:search", kwargs={"search_provider": "nada"})
        )

        self.assertEqual(response.status_code, 404)

    @patch_user_acl({"can_search": True, "can_search_users": False})
    def test_provider_no_permission(self):
        """provider raises 403 without permission"""
        response = self.client.get(
            reverse("misago:search", kwargs={"search_provider": "users"})
        )

        self.assertContains(
            response, "have permission to search users", status_code=403
        )

    def test_provider(self):
        """provider displays no script page"""
        response = self.client.get(
            reverse("misago:search", kwargs={"search_provider": "users"})
        )

        self.assertContains(response, "Loading search...")
