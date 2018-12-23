from django.urls import reverse

from ...users.test import AuthenticatedUserTestCase
from ..models import Agreement


class RequiredAgreementTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.test_link = reverse("misago:index")

        Agreement.objects.invalidate_cache()

    def tearDown(self):
        Agreement.objects.invalidate_cache()

    def test_tos_link(self):
        Agreement.objects.create(
            type=Agreement.TYPE_TOS, link="https://test-agreement.com", is_active=True
        )

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

    def test_tos_text(self):
        Agreement.objects.create(
            type=Agreement.TYPE_TOS, text="Lorem ipsum", is_active=True
        )

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

    def test_tos_text_and_link(self):
        Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            link="https://test-agreement.com",
            text="Lorem ipsum",
            is_active=True,
        )

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

    def test_privacy_link(self):
        Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link="https://test-agreement.com",
            is_active=True,
        )

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

    def test_privacy_text(self):
        Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY, text="Lorem ipsum", is_active=True
        )

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

    def test_privacy_text_and_link(self):
        Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link="https://test-agreement.com",
            text="Lorem ipsum",
            is_active=True,
        )

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

    def test_both(self):
        Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            link="https://test-agreement.com",
            text="Lorem ipsum",
            is_active=True,
        )

        Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link="https://test-agreement.com",
            text="Lorem ipsum",
            is_active=True,
        )

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)
