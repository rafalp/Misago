from django.test import TestCase
from django.urls import reverse

from ...conf.test import override_dynamic_settings


class AuthViewsTests(TestCase):
    def test_logout_view(self):
        """logout view logs user out on post"""
        response = self.client.post(
            "/api/auth/", data={"username": "nope", "password": "not-checked"}
        )

        self.assertContains(
            response, "Login or password is incorrect.", status_code=400
        )

        response = self.client.get("/api/auth/")
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertIsNone(user_json["id"])

        response = self.client.post(reverse("misago:logout"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get("/api/auth/")
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertIsNone(user_json["id"])

    def test_logout_view_return_302(self):
        """logout view should always return redirect"""
        response = self.client.get(reverse("misago:logout"))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse("misago:logout"))
        self.assertEqual(response.status_code, 302)
