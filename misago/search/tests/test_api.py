from django.urls import reverse
from django.utils import six

from misago.acl.testutils import override_acl
from misago.search.searchproviders import searchproviders
from misago.users.testutils import AuthenticatedUserTestCase


class SearchApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(SearchApiTests, self).setUp()

        self.test_link = reverse('misago:api:search')

    def test_no_permission(self):
        """api validates permission to search"""
        override_acl(self.user, {'can_search': 0})

        response = self.client.get(self.test_link)

        self.assertContains(response, "have permission to search site", status_code=403)

    def test_no_phrase(self):
        """api handles no search query"""
        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

        providers = searchproviders.get_providers(True)
        for i, provider in enumerate(response.json()):
            provider_api = reverse(
                'misago:api:search', kwargs={
                    'search_provider': providers[i].url,
                }
            )
            self.assertEqual(provider_api, provider['api'])

            self.assertEqual(six.text_type(providers[i].name), provider['name'])
            self.assertEqual(provider['results']['results'], [])
            self.assertEqual(int(provider['time']), 0)

    def test_empty_search(self):
        """api handles empty search query"""
        response = self.client.get('%s?q=' % self.test_link)
        self.assertEqual(response.status_code, 200)

        providers = searchproviders.get_providers(True)
        for i, provider in enumerate(response.json()):
            provider_api = reverse(
                'misago:api:search',
                kwargs={'search_provider': providers[i].url},
            )
            self.assertEqual(provider_api, provider['api'])

            self.assertEqual(six.text_type(providers[i].name), provider['name'])
            self.assertEqual(provider['results']['results'], [])
            self.assertEqual(int(provider['time']), 0)
