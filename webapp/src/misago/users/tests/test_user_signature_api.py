from ...acl.test import patch_user_acl
from ..test import AuthenticatedUserTestCase


class UserSignatureTests(AuthenticatedUserTestCase):
    """tests for user signature RPC (POST to /api/users/1/signature/)"""

    def setUp(self):
        super().setUp()
        self.link = "/api/users/%s/signature/" % self.user.pk

    @patch_user_acl({"can_have_signature": 0})
    def test_signature_no_permission(self):
        """edit signature api with no ACL returns 403"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You don't have permission to change signature."},
        )

    @patch_user_acl({"can_have_signature": 1})
    def test_signature_locked(self):
        """locked edit signature returns 403"""
        self.user.is_signature_locked = True
        self.user.signature_lock_user_message = "Your siggy is banned."
        self.user.save()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                "detail": "Your signature is locked. You can't change it.",
                "reason": "<p>Your siggy is banned.</p>",
            },
        )

    @patch_user_acl({"can_have_signature": 1})
    def test_get_signature(self):
        """GET to api returns json with no signature"""
        self.user.is_signature_locked = False
        self.user.save()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.json()["signature"])

    @patch_user_acl({"can_have_signature": 1})
    def test_post_empty_signature(self):
        """empty POST empties user signature"""
        self.user.is_signature_locked = False
        self.user.save()

        response = self.client.post(self.link, data={"signature": ""})
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.json()["signature"])

    @patch_user_acl({"can_have_signature": 1})
    def test_post_too_long_signature(self):
        """too long new signature errors"""
        self.user.is_signature_locked = False
        self.user.save()

        response = self.client.post(self.link, data={"signature": "abcd" * 1000})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Signature is too long."})

    @patch_user_acl({"can_have_signature": 1})
    def test_post_good_signature(self):
        """POST with good signature changes user signature"""
        self.user.is_signature_locked = False
        self.user.save()

        response = self.client.post(self.link, data={"signature": "Hello, **bros**!"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["signature"]["html"], "<p>Hello, <strong>bros</strong>!</p>"
        )
        self.assertEqual(response.json()["signature"]["plain"], "Hello, **bros**!")

        self.reload_user()
        self.assertEqual(
            self.user.signature_parsed, "<p>Hello, <strong>bros</strong>!</p>"
        )
