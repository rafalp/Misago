from django.test import TestCase
from django.urls import reverse

from ..test import create_test_user


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
        create_test_user("User", "user@example.com")

        # exact case sensitive match
        response = self.client.get(self.api_link + "?q=User")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"avatar": "http://placekitten.com/100/100", "username": "User"}],
        )

        # case insensitive match
        response = self.client.get(self.api_link + "?q=user")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"avatar": "http://placekitten.com/100/100", "username": "User"}],
        )

        # eager case insensitive match
        response = self.client.get(self.api_link + "?q=u")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"avatar": "http://placekitten.com/100/100", "username": "User"}],
        )

        # invalid match
        response = self.client.get(self.api_link + "?q=other")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
