import warnings

from django.test import TestCase

from misago.core import SUPPORTED_ENGINES, check_db_engine


INVALID_ENGINES = [
    'django.db.backends.sqlite3',
    'django.db.backends.mysql',
    'django.db.backends.oracle',
]


class TestCheckDBEngine(TestCase):
    def test_valid_engines(self):
        """check passes valid engines"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            for engine in SUPPORTED_ENGINES:
                with self.settings(DATABASES={'default': {'ENGINE': engine}}):
                    errors = check_db_engine(None)
                    self.assertEqual(errors, [])

    def test_invalid_engines(self):
        """check returns error for invalid engines"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            for engine in INVALID_ENGINES:
                with self.settings(DATABASES={'default': {'ENGINE': engine}}):
                    errors = check_db_engine(None)
                    self.assertTrue(errors)
