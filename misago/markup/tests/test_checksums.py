from django.test import TestCase

from .. import checksums


class ChecksumsTests(TestCase):
    def test_checksums(self):
        fake_message = "<p>Woow, thats awesome!</p>"
        post_pk = 231

        checksum = checksums.make_checksum(fake_message, [post_pk])

        self.assertTrue(checksums.is_checksum_valid(fake_message, checksum, [post_pk]))
        self.assertFalse(checksums.is_checksum_valid(fake_message, checksum, [3]))
