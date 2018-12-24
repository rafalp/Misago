from django.urls import reverse

from ...users.test import AuthenticatedUserTestCase


class ParseMarkupApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.api_link = reverse("misago:api:parse-markup")

    def test_is_anonymous(self):
        """api requires authentication"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

    def test_no_data(self):
        """api handles no data"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "You have to enter a message."})

    def test_invalid_data(self):
        """api handles post that is invalid type"""
        response = self.client.post(
            self.api_link, "[]", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Invalid data. Expected a dictionary, but got list."},
        )

        response = self.client.post(
            self.api_link, "123", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Invalid data. Expected a dictionary, but got int."},
        )

        response = self.client.post(
            self.api_link, '"string"', content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Invalid data. Expected a dictionary, but got str."},
        )

        response = self.client.post(
            self.api_link, "malformed", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "JSON parse error - Expecting value: line 1 column 1 (char 0)"},
        )

    def test_empty_post(self):
        """api handles empty post"""
        response = self.client.post(self.api_link, {"post": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "You have to enter a message."})

        # regression test for #929
        response = self.client.post(self.api_link, {"post": "\n"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "You have to enter a message."})

    def test_invalid_post(self):
        """api handles invalid post type"""
        response = self.client.post(self.api_link, {"post": 123})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "Posted message should be at least 5 characters long (it has 3)."
                )
            },
        )

    def test_valid_post(self):
        """api returns parsed markup for valid post"""
        response = self.client.post(self.api_link, {"post": "Lorem ipsum dolor met!"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"parsed": "<p>Lorem ipsum dolor met!</p>"})
