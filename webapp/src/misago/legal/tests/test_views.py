from django.test import TestCase
from django.urls import reverse

from ..models import Agreement


class PrivacyPolicyTests(TestCase):
    def setUp(self):
        Agreement.objects.invalidate_cache()

    def tearDown(self):
        Agreement.objects.invalidate_cache()

    def test_404_on_no_policy(self):
        """policy view returns 404 when no policy is set"""
        response = self.client.get(reverse("misago:privacy-policy"))
        self.assertEqual(response.status_code, 404)

    def test_301_on_link_policy(self):
        """policy view returns 302 redirect when link is set"""
        Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link="http://test.com",
            text="Lorem ipsum",
            is_active=True,
        )

        response = self.client.get(reverse("misago:privacy-policy"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "http://test.com")

    def test_200_on_link_policy(self):
        """policy view returns 200 when custom tos content is set"""
        Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            title="Test Policy",
            text="Lorem ipsum dolor",
            is_active=True,
        )

        response = self.client.get(reverse("misago:privacy-policy"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Policy")
        self.assertContains(response, "Lorem ipsum dolor")


class TermsOfServiceTests(TestCase):
    def setUp(self):
        Agreement.objects.invalidate_cache()

    def tearDown(self):
        Agreement.objects.invalidate_cache()

    def test_404_on_no_tos(self):
        """TOS view returns 404 when no TOS is set"""
        response = self.client.get(reverse("misago:terms-of-service"))
        self.assertEqual(response.status_code, 404)

    def test_301_on_link_tos(self):
        """TOS view returns 302 redirect when link is set"""
        Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            link="http://test.com",
            text="Lorem ipsum",
            is_active=True,
        )

        response = self.client.get(reverse("misago:terms-of-service"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "http://test.com")

    def test_200_on_link_tos(self):
        """TOS view returns 200 when custom tos content is set"""
        Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            title="Test ToS",
            text="Lorem ipsum dolor",
            is_active=True,
        )

        response = self.client.get(reverse("misago:terms-of-service"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test ToS")
        self.assertContains(response, "Lorem ipsum dolor")
