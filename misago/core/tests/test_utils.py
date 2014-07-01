#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from misago.core.utils import is_request_to_misago, slugify, time_amount


VALID_PATHS = (
    "/",
    "/threads/",
)

INVALID_PATHS = (
    "",
    "somewhere/",
)


class IsRequestToMisagoTests(TestCase):
    def test_is_request_to_misago(self):
        """
        is_request_to_misago correctly detects requests directed at Misago
        """
        misago_prefix = reverse('misago:index')

        for path in VALID_PATHS:
            request = RequestFactory().get('/')
            request.path_info = path
            self.assertTrue(
                is_request_to_misago(request),
                '"%s" is not overlapped by "%s"' % (path, misago_prefix))

        for path in INVALID_PATHS:
            request = RequestFactory().get('/')
            request.path_info = path
            self.assertFalse(
                is_request_to_misago(request),
                '"%s" is overlapped by "%s"' % (path, misago_prefix))


class SlugifyTests(TestCase):
    def test_valid_slugify_output(self):
        """Misago's slugify correcly slugifies string"""
        test_cases = (
            (u'Bob', u'bob'),
            (u'Eric The Fish', u'eric-the-fish'),
            (u'John   Snow', u'john-snow'),
            (u'J0n', u'j0n'),
            (u'An###ne', u'anne'),
            (u'S**t', u'st'),
            (u'Łók', u'lok'),
        )

        for original, slug in test_cases:
            self.assertEqual(slugify(original), slug)


class TimeAmountTests(TestCase):
    def test_single_units(self):
        """time_amount return correct amount of time for 1 precision"""
        self.assertEqual(time_amount(1), "1 second")
        self.assertEqual(time_amount(5), "5 seconds")
        self.assertEqual(time_amount(35), "35 seconds")

        self.assertEqual(time_amount(60), "1 minute")
        self.assertEqual(time_amount(120), "2 minutes")
        self.assertEqual(time_amount(240), "4 minutes")

        self.assertEqual(time_amount(3600), "1 hour")
        self.assertEqual(time_amount(7200), "2 hours")

        self.assertEqual(time_amount(24 * 3600), "1 day")
        self.assertEqual(time_amount(5 * 24 * 3600), "5 days")

    def test_double_units(self):
        """time_amount return correct amount of time for double precision"""
        self.assertEqual(time_amount(61), "1 minute and 1 second")
        self.assertEqual(time_amount(90), "1 minute and 30 seconds")

        self.assertEqual(time_amount(121), "2 minutes and 1 second")
        self.assertEqual(time_amount(150), "2 minutes and 30 seconds")

        self.assertEqual(time_amount(3660), "1 hour and 1 minute")
        self.assertEqual(time_amount(3720), "1 hour and 2 minutes")

        self.assertEqual(time_amount(24 * 3600 + 1), "1 day and 1 second")
        self.assertEqual(time_amount(2 * 24 * 3600 + 1), "2 days and 1 second")
        self.assertEqual(time_amount(2 * 24 * 3600 + 5),
                         "2 days and 5 seconds")

        self.assertEqual(time_amount(2 * 24 * 3600 + 3 * 3600),
                         "2 days and 3 hours")

    def test_triple_units(self):
        """time_amount return correct amount of time for triple precision"""
        self.assertEqual(time_amount(3661), "1 hour, 1 minute and 1 second")
        self.assertEqual(time_amount(2 * 3661),
                         "2 hours, 2 minutes and 2 seconds")
