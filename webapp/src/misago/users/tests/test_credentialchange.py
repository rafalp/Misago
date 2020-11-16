from django.test import TestCase

from ...users import credentialchange
from ..test import create_test_user


class MockRequest:
    def __init__(self, user):
        self.session = {}
        self.user = user


class CredentialChangeTests(TestCase):
    def setUp(self):
        self.user = create_test_user("User", "user@example.com")

    def test_valid_token_generation(self):
        """credentialchange module allows for store and read of change token"""
        request = MockRequest(self.user)
        token = credentialchange.store_new_credential(
            request, "email", "newmail@example.com"
        )

        email = credentialchange.read_new_credential(request, "email", token)
        self.assertEqual(email, "newmail@example.com")

    def test_email_change_invalidated_token(self):
        """token is invalidated by email change"""
        request = MockRequest(self.user)
        token = credentialchange.store_new_credential(
            request, "email", "newmail@example.com"
        )

        self.user.set_email("otheremail@example.com")
        self.user.save()

        email = credentialchange.read_new_credential(request, "email", token)
        self.assertIsNone(email)

    def test_password_change_invalidated_token(self):
        """token is invalidated by password change"""
        request = MockRequest(self.user)
        token = credentialchange.store_new_credential(
            request, "email", "newmail@example.com"
        )

        self.user.set_password("Egebeg!123")
        self.user.save()

        email = credentialchange.read_new_credential(request, "email", token)
        self.assertIsNone(email)

    def test_invalid_token_is_handled(self):
        """there are no explosions in invalid tokens handling"""
        request = MockRequest(self.user)
        token = credentialchange.store_new_credential(
            request, "email", "newmail@example.com"
        )

        email = credentialchange.read_new_credential(request, "em4il", token)
        self.assertIsNone(email)
