#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from misago.core.utils import (
    clean_return_path, format_plaintext_for_html, is_referer_local, is_request_to_misago,
    parse_iso8601_string, slugify, get_exception_message)


VALID_PATHS = ("/", "/threads/", )

INVALID_PATHS = ("", "somewhere/", )


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
                '"%s" is not overlapped by "%s"' % (path, misago_prefix)
            )

        for path in INVALID_PATHS:
            request = RequestFactory().get('/')
            request.path_info = path
            self.assertFalse(
                is_request_to_misago(request),
                '"%s" is overlapped by "%s"' % (path, misago_prefix)
            )


class SlugifyTests(TestCase):
    def test_valid_slugify_output(self):
        """Misago's slugify correctly slugifies string"""
        test_cases = [
            ('Bob', 'bob'),
            ('Eric The Fish', 'eric-the-fish'),
            ('John   Snow', 'john-snow'),
            ('J0n', 'j0n'),
            ('An###ne', 'anne'),
            ('S**t', 'st'),
            ('Łók', 'lok'),
        ]

        for original, slug in test_cases:
            self.assertEqual(slugify(original), slug)


class ParseIso8601StringTests(TestCase):
    def test_valid_input(self):
        """util parses iso 8601 strings"""
        INPUTS = [
            '2016-10-22T20:55:39.185085Z',
            '2016-10-22T20:55:39.185085-01:00',
            '2016-10-22T20:55:39-01:00',
            '2016-10-22T20:55:39.185085+01:00',
        ]

        for test_input in INPUTS:
            self.assertTrue(parse_iso8601_string(test_input))

    def test_invalid_input(self):
        """util throws ValueError on invalid input"""
        INPUTS = [
            '',
            '2016-10-22',
            '2016-10-22T30:55:39.185085+11:00',
            '2016-10-22T20:55:39.18SSSSS5085Z',
        ]

        for test_input in INPUTS:
            with self.assertRaises(ValueError):
                self.assertTrue(parse_iso8601_string(test_input))


PLAINTEXT_FORMAT_CASES = [
    ('Lorem ipsum.', '<p>Lorem ipsum.</p>'),
    ('Lorem <b>ipsum</b>.', '<p>Lorem &lt;b&gt;ipsum&lt;/b&gt;.</p>'),
    ('Lorem "ipsum" dolor met.', '<p>Lorem &quot;ipsum&quot; dolor met.</p>'),
    ('Lorem ipsum.\nDolor met.', '<p>Lorem ipsum.<br />Dolor met.</p>'),
    ('Lorem ipsum.\n\nDolor met.', '<p>Lorem ipsum.</p>\n\n<p>Dolor met.</p>'),
    (
        'http://misago-project.org/login/',
        '<p><a href="http://misago-project.org/login/">http://misago-project.org/login/</a></p>'
    ),
]


class FormatPlaintextForHtmlTests(TestCase):
    def test_format_plaintext_for_html(self):
        """format_plaintext_for_html correctly formats plaintext for html"""
        for plaintext, html in PLAINTEXT_FORMAT_CASES:
            output = format_plaintext_for_html(plaintext)

            assertion_message = """
format_plaintext_for_html failed to produce expected output:

expected:   %s
return:     %s
""" % (html, output)
            self.assertEqual(output, html, assertion_message)


class MockRequest(object):
    scheme = 'http'

    def __init__(self, method, meta=None, post=None):
        self.method = method
        self.META = meta or {}
        self.POST = post or {}


class CleanReturnPathTests(TestCase):
    def test_get_request(self):
        """clean_return_path works for GET requests"""
        bad_request = MockRequest(
            'GET', {
                'HTTP_REFERER': 'http://cookies.com',
                'HTTP_HOST': 'misago-project.org',
            }
        )
        self.assertIsNone(clean_return_path(bad_request))

        bad_request = MockRequest(
            'GET', {
                'HTTP_REFERER': 'https://misago-project.org/',
                'HTTP_HOST': 'misago-project.org/',
            }
        )
        self.assertIsNone(clean_return_path(bad_request))

        bad_request = MockRequest(
            'GET', {
                'HTTP_REFERER': 'https://misago-project.org/',
                'HTTP_HOST': 'misago-project.org/assadsa/',
            }
        )
        self.assertIsNone(clean_return_path(bad_request))

        ok_request = MockRequest(
            'GET', {
                'HTTP_REFERER': 'http://misago-project.org/',
                'HTTP_HOST': 'misago-project.org/',
            }
        )
        self.assertEqual(clean_return_path(ok_request), '/')

        ok_request = MockRequest(
            'GET', {
                'HTTP_REFERER': 'http://misago-project.org/login/',
                'HTTP_HOST': 'misago-project.org/',
            }
        )
        self.assertEqual(clean_return_path(ok_request), '/login/')

    def test_post_request(self):
        """clean_return_path works for POST requests"""
        bad_request = MockRequest(
            'POST', {
                'HTTP_REFERER': 'http://misago-project.org/',
                'HTTP_HOST': 'misago-project.org/',
            }, {
                'return_path': '/sdasdsa/',
            }
        )
        self.assertIsNone(clean_return_path(bad_request))

        ok_request = MockRequest(
            'POST', {
                'HTTP_REFERER': 'http://misago-project.org/',
                'HTTP_HOST': 'misago-project.org/',
            }, {
                'return_path': '/login/',
            }
        )
        self.assertEqual(clean_return_path(ok_request), '/login/')


class IsRefererLocalTests(TestCase):
    def test_local_referers(self):
        """local referers return true"""
        ok_request = MockRequest(
            'GET', {
                'HTTP_REFERER': 'http://misago-project.org/',
                'HTTP_HOST': 'misago-project.org/',
            }
        )
        self.assertTrue(is_referer_local(ok_request))

        ok_request = MockRequest(
            'GET', {
                'HTTP_REFERER': 'http://misago-project.org/',
                'HTTP_HOST': 'misago-project.org/',
            }
        )
        self.assertTrue(is_referer_local(ok_request))

        ok_request = MockRequest(
            'GET', {
                'HTTP_REFERER': 'http://misago-project.org/login/',
                'HTTP_HOST': 'misago-project.org/',
            }
        )
        self.assertTrue(is_referer_local(ok_request))

    def test_foreign_referers(self):
        """non-local referers return false"""
        bad_request = MockRequest(
            'GET', {
                'HTTP_REFERER': 'http://else-project.org/',
                'HTTP_HOST': 'misago-project.org/',
            }
        )
        self.assertFalse(is_referer_local(bad_request))

        bad_request = MockRequest(
            'GET', {
                'HTTP_REFERER': 'https://misago-project.org/',
                'HTTP_HOST': 'misago-project.org/',
            }
        )
        self.assertFalse(is_referer_local(bad_request))

        bad_request = MockRequest(
            'GET', {
                'HTTP_REFERER': 'http://misago-project.org/',
                'HTTP_HOST': 'misago-project.org/assadsa/',
            }
        )
        self.assertFalse(is_referer_local(bad_request))


class GetExceptionMessageTests(TestCase):
    def test_no_args(self):
        """both of helper args are optional"""
        message = get_exception_message()
        self.assertIsNone(message)

    def test_no_default_message(self):
        """helper's default message arg is optional"""
        message = get_exception_message(PermissionDenied('Lorem Ipsum'))
        self.assertEqual(message, 'Lorem Ipsum')

        message = get_exception_message(PermissionDenied())
        self.assertIsNone(message)

    def test_default_message(self):
        """helper's default message arg is used"""
        message = get_exception_message(PermissionDenied('Lorem Ipsum'), 'Default')
        self.assertEqual(message, 'Lorem Ipsum')

        message = get_exception_message(PermissionDenied(), 'Default')
        self.assertEqual(message, 'Default')

        message = get_exception_message(default_message='Lorem Ipsum')
        self.assertEqual(message, 'Lorem Ipsum')
