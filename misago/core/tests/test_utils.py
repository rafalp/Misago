#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from misago.core.utils import is_request_to_misago, slugify


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
        )

        for original, slug in test_cases:
            self.assertEqual(slugify(original), slug)
