#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone

from misago.core.utils import (clean_return_path, is_request_to_misago,
                               slugify, is_referer_local,
                               format_plaintext_for_html)


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
        """Misago's slugify correctly slugifies string"""
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


PLAINTEXT_FORMAT_CASES = (
    (
        u'Lorem ipsum.',
        u'<p>Lorem ipsum.</p>'
    ),
    (
        u'Lorem <b>ipsum</b>.',
        u'<p>Lorem &lt;b&gt;ipsum&lt;/b&gt;.</p>'
    ),
    (
        u'Lorem "ipsum" dolor met.',
        u'<p>Lorem &quot;ipsum&quot; dolor met.</p>'
    ),
    (
        u'Lorem ipsum.\nDolor met.',
        u'<p>Lorem ipsum.<br />Dolor met.</p>'
    ),
    (
        u'Lorem ipsum.\n\nDolor met.',
        u'<p>Lorem ipsum.</p>\n\n<p>Dolor met.</p>'
    ),
    (
        u'http://misago-project.org/login/',
        u'<p><a href="http://misago-project.org/login/">http://misago-project.org/login/</a></p>'
    ),
)


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
        bad_request = MockRequest('GET', {
            'HTTP_REFERER': 'http://cookies.com',
            'HTTP_HOST': 'misago-project.org'
        })
        self.assertIsNone(clean_return_path(bad_request))

        bad_request = MockRequest('GET', {
            'HTTP_REFERER': 'https://misago-project.org/',
            'HTTP_HOST': 'misago-project.org/'
        })
        self.assertIsNone(clean_return_path(bad_request))

        bad_request = MockRequest('GET', {
            'HTTP_REFERER': 'https://misago-project.org/',
            'HTTP_HOST': 'misago-project.org/assadsa/'
        })
        self.assertIsNone(clean_return_path(bad_request))

        ok_request = MockRequest('GET', {
            'HTTP_REFERER': 'http://misago-project.org/',
            'HTTP_HOST': 'misago-project.org/'
        })
        self.assertEqual(clean_return_path(ok_request), '/')

        ok_request = MockRequest('GET', {
            'HTTP_REFERER': 'http://misago-project.org/login/',
            'HTTP_HOST': 'misago-project.org/'
        })
        self.assertEqual(clean_return_path(ok_request), '/login/')

    def test_post_request(self):
        """clean_return_path works for POST requests"""
        bad_request = MockRequest('POST', {
            'HTTP_REFERER': 'http://misago-project.org/',
            'HTTP_HOST': 'misago-project.org/'
        }, {'return_path': '/sdasdsa/'})
        self.assertIsNone(clean_return_path(bad_request))

        ok_request = MockRequest('POST', {
            'HTTP_REFERER': 'http://misago-project.org/',
            'HTTP_HOST': 'misago-project.org/'
        }, {'return_path': '/login/'})
        self.assertEqual(clean_return_path(ok_request), '/login/')


class IsRefererLocalTests(TestCase):
    def test_local_referers(self):
        """local referers return true"""
        ok_request = MockRequest('GET', {
            'HTTP_REFERER': 'http://misago-project.org/',
            'HTTP_HOST': 'misago-project.org/'
        })
        self.assertTrue(is_referer_local(ok_request))

        ok_request = MockRequest('GET', {
            'HTTP_REFERER': 'http://misago-project.org/',
            'HTTP_HOST': 'misago-project.org/'
        })
        self.assertTrue(is_referer_local(ok_request))

        ok_request = MockRequest('GET', {
            'HTTP_REFERER': 'http://misago-project.org/login/',
            'HTTP_HOST': 'misago-project.org/'
        })
        self.assertTrue(is_referer_local(ok_request))

    def test_foreign_referers(self):
        """non-local referers return false"""
        bad_request = MockRequest('GET', {
            'HTTP_REFERER': 'http://else-project.org/',
            'HTTP_HOST': 'misago-project.org/'
        })
        self.assertFalse(is_referer_local(bad_request))

        bad_request = MockRequest('GET', {
            'HTTP_REFERER': 'https://misago-project.org/',
            'HTTP_HOST': 'misago-project.org/'
        })
        self.assertFalse(is_referer_local(bad_request))

        bad_request = MockRequest('GET', {
            'HTTP_REFERER': 'http://misago-project.org/',
            'HTTP_HOST': 'misago-project.org/assadsa/'
        })
        self.assertFalse(is_referer_local(bad_request))
