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
        response = self.client.get("%s?q=%s" % (self.api_link, self.user.username))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn("users", [p["id"] for p in response_json])

        for provider in response_json:
            if provider["id"] == "users":
                results = provider["results"]["results"]
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["id"], self.user.id)

    def test_orphans_match(self):
        """api handles last three chars match query"""
        response = self.client.get("%s?q=%s" % (self.api_link, self.user.username[-3:]))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn("users", [p["id"] for p in response_json])

        for provider in response_json:
            if provider["id"] == "users":
                results = provider["results"]["results"]
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["id"], self.user.id)

    def test_no_match(self):
        """api handles no match"""
        response = self.client.get("%s?q=BobBoberson" % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn("users", [p["id"] for p in response_json])

        for provider in response_json:
            if provider["id"] == "users":
                self.assertEqual(provider["results"]["results"], [])

    def test_search_disabled_user(self):
        """api respects disabled users visibility"""
        disabled_user = create_test_user(
            "DisabledUser", "disableduser@example.com", is_active=False
        )

        response = self.client.get("%s?q=DisabledUser" % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn("users", [p["id"] for p in response_json])

        for provider in response_json:
            if provider["id"] == "users":
                self.assertEqual(provider["results"]["results"], [])

        # user shows in searchech performed by staff
        self.user.is_staff = True
        self.user.save()

        response = self.client.get("%s?q=DisabledUser" % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn("users", [p["id"] for p in response_json])

        for provider in response_json:
            if provider["id"] == "users":
                results = provider["results"]["results"]
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["id"], disabled_user.id)


class SearchProviderApiTests(SearchApiTests):
    def setUp(self):
        super().setUp()

        self.api_link = reverse(
            "misago:api:search", kwargs={"search_provider": "users"}
        )
