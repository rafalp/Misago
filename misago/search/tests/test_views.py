from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.threads.search import SearchThreads
from misago.users.testutils import AuthenticatedUserTestCase


class LandingTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(LandingTests, self).setUp()

        self.test_link = reverse('misago:search')

    def test_no_permission(self):
        """view validates permission to search forum"""
        override_acl(self.user, {'can_search': 0})

        response = self.client.get(self.test_link)

        self.assertContains(response, "have permission to search site", status_code=403)

    def test_redirect_to_provider(self):
        """view validates permission to search forum"""
        response = self.client.get(self.test_link)

        self.assertEqual(response.status_code, 302)
        self.assertIn(SearchThreads.url, response['location'])


class SearchTests(AuthenticatedUserTestCase):
    def test_no_permission(self):
        """view validates permission to search forum"""
        override_acl(self.user, {'can_search': 0})

        response = self.client.get(reverse('misago:search', kwargs={'search_provider': 'users'}))

        self.assertContains(response, "have permission to search site", status_code=403)

    def test_not_found(self):
        """view raises 404 for not found provider"""
        response = self.client.get(reverse('misago:search', kwargs={'search_provider': 'nada'}))

        self.assertEqual(response.status_code, 404)

    def test_provider_no_permission(self):
        """provider raises 403 without permission"""
        override_acl(self.user, {'can_search_users': 0})

        response = self.client.get(reverse('misago:search', kwargs={'search_provider': 'users'}))

        self.assertContains(response, "have permission to search users", status_code=403)

    def test_provider(self):
        """provider displays no script page"""
        response = self.client.get(reverse('misago:search', kwargs={'search_provider': 'threads'}))

        self.assertContains(response, "Loading search...")
