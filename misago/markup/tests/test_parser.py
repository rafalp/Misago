# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from ..parser import parse


class MockRequest(object):
    scheme = 'http'

    def get_host(self):
        return 'test.com'


class MockPoster(object):
    pass


class BBCodeTests(TestCase):
    def test_inline_text(self):
        """inline elements are correctly parsed"""
        test_text = """
Lorem **ipsum** dolor met.

Lorem [b]ipsum[/b] [i]dolor[/i] [u]met[/u].

Lorem [b]**ipsum**[/b] [i]dolor[/i] [u]met[/u].

Lorem [b]**ipsum[/b]** [i]dolor[/i] [u]met[/u].

Lorem [b]__ipsum[/b]__ [i]dolor[/i] [u]met[/u].

Lorem [b][i]ipsum[/i][/b].

Lorem [b][i]ipsum[/b][/i].

Lorem [b]ipsum[/B].
""".strip()

        expected_result = """
<p>Lorem <strong>ipsum</strong> dolor met.</p>
<p>Lorem <b>ipsum</b> <i>dolor</i> <u>met</u>.</p>
<p>Lorem <b><strong>ipsum</strong></b> <i>dolor</i> <u>met</u>.</p>
<p>Lorem <b>**ipsum</b>** <i>dolor</i> <u>met</u>.</p>
<p>Lorem <b>__ipsum</b>__ <i>dolor</i> <u>met</u>.</p>
<p>Lorem <b><i>ipsum</i></b>.</p>
<p>Lorem <b>[i]ipsum</b>[/i].</p>
<p>Lorem <b>ipsum</b>.</p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_blocks(self):
        """block elements are correctly parsed"""
        test_text = """
Lorem ipsum.
[hR]
Dolor met.
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<hr/>
<p>Dolor met.</p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])


class MinifyTests(TestCase):
    def test_minified_text(self):
        """parser minifies text successfully"""
        test_text = """
Lorem ipsum.

Lorem ipsum.
""".strip()

        expected_result = """
<p>Lorem ipsum.</p><p>Lorem ipsum.</p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_minified_unicode_text(self):
        """parser minifies unicode text successfully"""
        test_text = """
Bżęczyszczykiewłicz ipsum.

Lorem ipsum.
""".strip()

        expected_result = """
<p>Bżęczyszczykiewłicz ipsum.</p><p>Lorem ipsum.</p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])


class CleanLinksTests(TestCase):
    def test_clean_current_link(self):
        """clean_links step leaves http://test.com alone"""
        test_text = """
Lorem ipsum: http://test.com
""".strip()

        expected_result = """
<p>Lorem ipsum: <a href="/" rel="nofollow">test.com</a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_trim_current_path(self):
        """clean_links step leaves http://test.com path"""
        test_text = """
Lorem ipsum: http://test.com/somewhere-something/
""".strip()

        expected_result = """
<p>Lorem ipsum: <a href="/somewhere-something/" rel="nofollow">test.com/somewhere-something/</a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_clean_outgoing_link_domain(self):
        """clean_links step leaves outgoing domain link"""
        test_text = """
Lorem ipsum: http://somewhere.com
""".strip()

        expected_result = """
<p>Lorem ipsum: <a href="http://somewhere.com" rel="nofollow">somewhere.com</a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_trim_outgoing_path(self):
        """clean_links step leaves outgoing link domain and path"""
        test_text = """
Lorem ipsum: http://somewhere.com/somewhere-something/
""".strip()

        expected_result = """
<p>Lorem ipsum: <a href="http://somewhere.com/somewhere-something/" rel="nofollow">somewhere.com/somewhere-something/</a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_clean_local_image_src(self):
        """clean_links step cleans local image src"""
        test_text = """
!(http://test.com/image.jpg)
""".strip()

        expected_result = """
<p><img alt="test.com/image.jpg" src="/image.jpg"/></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_clean_remote_image_src(self):
        """clean_links step cleans remote image src"""
        test_text = """
!(http://somewhere.com/image.jpg)
""".strip()

        expected_result = """
<p><img alt="somewhere.com/image.jpg" src="http://somewhere.com/image.jpg"/></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])
