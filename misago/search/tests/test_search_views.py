from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.users.testutils import AuthenticatedUserTestCase


class LandingTests(AuthenticatedUserTestCase):
    """
    todo:

    - no search providers registered
    - no search providers allowed
    - redirect to first search provider
    """
    def setUp(self):
        super(LandingTests, self).setUp()

        self.test_link = reverse('misago:search')

    def test_no_permission(self):
        """view validates permission to search forum"""
        override_acl(self.user, {
            'can_search': 0
        })

        response = self.client.get(self.test_link)
        self.assertContains(
            response, "have permission to search site", status_code=403)


class SearchTests(AuthenticatedUserTestCase):
    """
    todo:

    - no search providers registered
    - search provider name not found
    - search provider disallowed
    - noscript view displayed
    """
    def test_no_permission(self):
        """view validates permission to search forum"""
        override_acl(self.user, {
            'can_search': 0
        })

        response = self.client.get(
            reverse('misago:search', kwargs={'search_provider': 'users'}))
        self.assertContains(
            response, "have permission to search site", status_code=403)
