from django.test import TestCase
from misago.users.utils import hash_email


class UserModelTests(TestCase):
    def test_hash_email_works(self):
        """hash email produces repeatable outcomes"""
        self.assertEqual(hash_email('abc@test.com'),
                         hash_email('aBc@tEst.cOm'))
