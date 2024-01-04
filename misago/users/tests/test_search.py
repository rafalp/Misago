import json

from django.urls import reverse

from ...acl.test import patch_user_acl
from ..test import AuthenticatedUserTestCase, create_test_user


class SearchApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.api_link = reverse("misago:api:search")

    @patch_user_acl({"can_search_users": 0})
    def test_no_permission(self):
        """api respects permission to search users"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("users", [p["id"] for p in response.json()])

    def test_no_query(self):
        """api handles no search query"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn("users", [p["id"] for p in response_json])

        for provider in response_json:
            if provider["id"] == "users":
                self.assertEqual(provider["results"]["results"], [])

    def test_empty_query(self):
        """api handles empty search query"""
        response = self.client.get("%s?q=" % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn("users", [p["id"] for p in response_json])

        for provider in response_json:
            if provider["id"] == "users":
                self.assertEqual(provider["results"]["results"], [])

    def test_short_query(self):
        """api handles short search query"""
        response = self.client.get("%s?q=%s" % (self.api_link, self.user.username[0]))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn("users", [p["id"] for p in response_json])

        for provider in response_json:
            if provider["id"] == "users":
                results = provider["results"]["results"]
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["id"], self.user.id)

    def test_exact_match(self):
        """api handles exact search query"""
        other_user = create_test_user("Other_User", "otheruser@example.com")

        response = self.client.get("%s?q=%s" % (self.api_link, other_user.username))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn("users", [p["id"] for p in response_json])

        for provider in response_json:
            if provider["id"] == "users":
                results = provider["results"]["results"]
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["id"], other_user.id)

    def test_orphans_match(self):
        """api handles last three chars match query"""
        other_user = create_test_user("Other_User", "otheruser@example.com")

        response = self.client.get("%s?q=%s" % (self.api_link, "Other_"))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn("users", [p["id"] for p in response_json])

        for provider in response_json:
            if provider["id"] == "users":
                results = provider["results"]["results"]
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["id"], other_user.id)

    def test_no_match(self):
        """api handles no match"""
        response = self.client.get("%s?q=BobBoberson" % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn("users", [p["id"] for p in response_json])

        for provider in response_json:
            if provider["id"] == "users":
                self.assertEqual(provider["results"]["results"], [])


def search_users(client, query=None):
    api_link = reverse("misago:api:search")
    if query:
        api_link += f"?q={query}"

    response = client.get(api_link)
    assert response.status_code == 200

    for search_results in json.loads(response.content):
        if search_results["id"] == "users":
            return search_results["results"]["results"]

    raise AssertionError("Search results did not include users!")


def test_search_users_api_excludes_deactivated_users(client, inactive_user):
    results = search_users(client, inactive_user.username)
    assert results == []


def test_search_users_api_includes_deactivated_users_if_client_is_admin(
    admin_client, inactive_user
):
    results = search_users(admin_client, inactive_user.username)
    assert results[0]["id"] == inactive_user.id


class SearchProviderApiTests(SearchApiTests):
    def setUp(self):
        super().setUp()

        self.api_link = reverse(
            "misago:api:search", kwargs={"search_provider": "users"}
        )
