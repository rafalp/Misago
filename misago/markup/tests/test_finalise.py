# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from ..finalise import finalise_markup


class QuoteTests(TestCase):
    def test_finalise_markup(self):
        """quote header is replaced"""
        test_text = '''
<p>Lorem ipsum.</p>
<blockquote>
<header></header>
<p>Dolor met</p>
<blockquote>
<header><a href="/users/bob-1/">@Bob</a></header>
<p>Dolor met</p>
</blockquote>
</blockquote>
<p>Lorem ipsum dolor.</>
'''.strip()

        expected_result = '''
<p>Lorem ipsum.</p>
<blockquote>
<header>Quoted message:</header>
<p>Dolor met</p>
<blockquote>
<header><a href="/users/bob-1/">@Bob</a> has written:</header>
<p>Dolor met</p>
</blockquote>
</blockquote>
<p>Lorem ipsum dolor.</>
'''.strip()

        self.assertEqual(expected_result, finalise_markup(test_text))

    def test_finalise_minified_markup(self):
        """header is replaced in minified post"""
        test_text = '''
<p>Lorem ipsum.</p><blockquote><header><a href="/users/bob-1/">@Bob</a></header><p>Dolor met</p></blockquote>
'''.strip()

        expected_result = '''
<p>Lorem ipsum.</p><blockquote><header><a href="/users/bob-1/">@Bob</a> has written:</header><p>Dolor met</p></blockquote>
'''.strip()

        self.assertEqual(expected_result, finalise_markup(test_text))
