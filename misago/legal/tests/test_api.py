import json

from django.urls import reverse

from ...users.test import AuthenticatedUserTestCase
from ..models import Agreement


class SubmitAgreementTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.agreement = Agreement.objects.create(
            type=Agreement.TYPE_TOS, text="Lorem ipsum", is_active=True
        )

        self.api_link = reverse(
            "misago:api:submit-agreement", kwargs={"pk": self.agreement.pk}
        )

    def post_json(self, data):
        return self.client.post(
            self.api_link, json.dumps(data), content_type="application/json"
        )

    def test_anonymous(self):
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

    def test_get_request(self):
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"detail": 'Method "GET" not allowed.'})

    def test_invalid_agreement_id(self):
        api_link = reverse(
            "misago:api:submit-agreement", kwargs={"pk": self.agreement.pk + 1}
        )

        response = self.client.post(api_link)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Not found."})

    def test_agreement_already_accepted(self):
        self.user.agreements.append(self.agreement.id)
        self.user.save()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You have already accepted this agreement."}
        )

    def test_no_accept_sent(self):
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You need to submit a valid choice."}
        )

    def test_invalid_accept_sent(self):
        response = self.post_json({"accept": 1})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You need to submit a valid choice."}
        )

    def test_accept_false(self):
        response = self.post_json({"accept": False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "ok"})

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_deleting_account)
        self.assertFalse(self.user.is_active)

    def test_accept_false_staff(self):
        self.user.is_staff = True
        self.user.save()

        response = self.post_json({"accept": False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "ok"})

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_deleting_account)
        self.assertTrue(self.user.is_active)

    def test_accept_true(self):
        response = self.post_json({"accept": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "ok"})

        self.user.refresh_from_db()
        self.assertEqual(self.user.agreements, [self.agreement.id])
        self.assertFalse(self.user.is_deleting_account)
        self.assertTrue(self.user.is_active)
