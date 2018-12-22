from django.test import TestCase
from django.urls import reverse

from misago.conf import settings
from misago.users.testutils import create_test_user


class AuthenticateApiTests(TestCase):
    def setUp(self):
        self.api_link = reverse("misago:api:mention-suggestions")

    def test_no_query(self):
        """api returns empty result set if no query is given"""
        response = self.client.get(self.api_link)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_no_results(self):
        """api returns empty result set if no query is given"""
        response = self.client.get(self.api_link + "?q=none")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_user_search(self):
        """api searches uses"""
        create_test_user("BobBoberson", "bob@test.com")

        # exact case sensitive match
        response = self.client.get(self.api_link + "?q=BobBoberson")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"avatar": "http://placekitten.com/100/100", "username": "BobBoberson"}],
        )

        # rought case insensitive match
        response = self.client.get(self.api_link + "?q=bob")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"avatar": "http://placekitten.com/100/100", "username": "BobBoberson"}],
        )

        # eager case insensitive match
        response = self.client.get(self.api_link + "?q=b")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"avatar": "http://placekitten.com/100/100", "username": "BobBoberson"}],
        )

        # invalid match
        response = self.client.get(self.api_link + "?q=bu")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
