from django.urls import reverse

from ...acl.test import patch_user_acl
from ...users.test import AuthenticatedUserTestCase
from ..searchproviders import searchproviders


class SearchApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.test_link = reverse("misago:api:search")

    @patch_user_acl({"can_search": False})
    def test_no_permission(self):
        """api validates permission to search"""
        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You don't have permission to search site."}
        )

    def test_no_phrase(self):
        """api handles no search query"""
        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

        providers = searchproviders.get_providers(True)
        for i, provider in enumerate(response.json()):
            provider_api = reverse(
                "misago:api:search", kwargs={"search_provider": providers[i].url}
            )
            self.assertEqual(provider_api, provider["api"])

            self.assertEqual(str(providers[i].name), provider["name"])
            self.assertEqual(provider["results"]["results"], [])
            self.assertEqual(int(provider["time"]), 0)

    def test_empty_search(self):
        """api handles empty search query"""
        response = self.client.get("%s?q=" % self.test_link)
        self.assertEqual(response.status_code, 200)

        providers = searchproviders.get_providers(True)
        for i, provider in enumerate(response.json()):
            provider_api = reverse(
                "misago:api:search", kwargs={"search_provider": providers[i].url}
            )
            self.assertEqual(provider_api, provider["api"])

            self.assertEqual(str(providers[i].name), provider["name"])
            self.assertEqual(provider["results"]["results"], [])
            self.assertEqual(int(provider["time"]), 0)
