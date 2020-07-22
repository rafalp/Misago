from django.test import TestCase

from ..utils import hash_email, gen_suffix_username


class HashEmailTests(TestCase):
    def test_is_case_insensitive(self):
        """util is case insensitive"""
        self.assertEqual(hash_email("abc@test.com"), hash_email("aBc@tEst.cOm"))

    def test_handles_unicode(self):
        """util works with unicode strings"""
        self.assertEqual(hash_email("łóć@test.com"), hash_email("ŁÓĆ@tEst.cOm"))


def test_gen_suffix_username():
    assert gen_suffix_username() != ""


def test_gen_suffix_username_len():
    assert len(gen_suffix_username()) == 8
