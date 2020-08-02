from django.test import TestCase

from ..utils import hash_email, suffix_taken_username


class HashEmailTests(TestCase):
    def test_is_case_insensitive(self):
        """util is case insensitive"""
        self.assertEqual(hash_email("abc@test.com"), hash_email("aBc@tEst.cOm"))

    def test_handles_unicode(self):
        """util works with unicode strings"""
        self.assertEqual(hash_email("łóć@test.com"), hash_email("ŁÓĆ@tEst.cOm"))


def test_suffix_taken_username():
    assert suffix_taken_username() != ""


def test_suffix_taken_username_len():
    assert len(suffix_taken_username()) == 8
