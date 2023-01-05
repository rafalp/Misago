from django.test import TestCase
from django.urls import reverse

from ...conf.test import override_dynamic_settings


class AuthViewsTests(TestCase):
    def test_auth_views_return_302(self):
        """auth views should always return redirect"""
        response = self.client.get(reverse("misago:login"))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse("misago:login"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("misago:logout"))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse("misago:logout"))
        self.assertEqual(response.status_code, 302)

    def test_login_view_redirect_to(self):
        """login view respects redirect_to POST"""
        # valid redirect
        response = self.client.post(
            reverse("misago:login"), data={"redirect_to": "/redirect/"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/redirect/?ref=login")

        # invalid redirect (redirects to other site)
        response = self.client.post(
            reverse("misago:login"),
            data={"redirect_to": "http://somewhereelse.com/page.html"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

        # invalid redirect (link name)
        response = self.client.post(
            reverse("misago:login"), data={"redirect_to": "misago:users"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

        # invalid redirect (non url)
        response = self.client.post(
            reverse("misago:login"), data={"redirect_to": "canada goose not url!"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

        # invalid redirect (unicode)
        response = self.client.post(
            reverse("misago:login"), data={"redirect_to": "łelcome!"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

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


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_provider="Lorem",
)
def test_login_view_returns_403_if_oauth_is_enabled(db, client):
    response = client.get(reverse("misago:login"))
    assert response.status_code == 403
