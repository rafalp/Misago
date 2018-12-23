import warnings

from django.test import TestCase

from ..deprecations import RemovedInMisagoWarning, warn


class DeprecationsTests(TestCase):
    def test_deprecations_warn(self):
        """deprecation utility raises warning"""
        with warnings.catch_warnings(record=True) as warning:
            warn("test warning")

            self.assertEqual(len(warning), 1)
            self.assertEqual(str(warning[0].message), "test warning")
            self.assertTrue(issubclass(warning[0].category, RemovedInMisagoWarning))
