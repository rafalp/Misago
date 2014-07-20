from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.users import signatures


class SignaturesTests(TestCase):
    def test_signature_change(self):
        """signature module allows for signature change"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@bob.com', 'pass123')

        signatures.set_user_signature(test_user, '')

        self.assertEqual(test_user.signature, '')
        self.assertEqual(test_user.signature_parsed, '')
        self.assertEqual(test_user.signature_checksum, '')

        signatures.set_user_signature(test_user, 'Hello, world!')

        self.assertEqual(test_user.signature, 'Hello, world!')
        self.assertEqual(test_user.signature_parsed, '<p>Hello, world!</p>')
        self.assertTrue(signatures.is_user_signature_valid(test_user))

        test_user.signature_parsed = '<p>Injected evil HTML!</p>'
        self.assertFalse(signatures.is_user_signature_valid(test_user))
