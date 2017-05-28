# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.markup.parser import parse


UserModel = get_user_model()


class MockRequest(object):
    scheme = 'http'

    def __init__(self, user=None):
        self.user = user

    def get_host(self):
        return 'test.com'


class MockPoster(object):
    username = 'LoremIpsum'
    slug = 'loremipsum'


class HTMLTests(TestCase):
    def test_html_escaped(self):
        """parser escapes all html"""
        test_text = """
Lorem <strong>ipsum!</strong>
""".strip()

        expected_result = """
<p>Lorem &lt;strong&gt;ipsum!&lt;/strong&gt;</p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])
        self.assertEqual(result['internal_links'], [])
        self.assertEqual(result['images'], [])
        self.assertEqual(result['outgoing_links'], [])


class BBCodeTests(TestCase):
    def test_inline_text(self):
        """inline elements are correctly parsed"""
        test_text = """
Lorem **ipsum**, dolor met.

Lorem [b]ipsum[/b], [i]dolor[/i] [u]met[/u].

Lorem [b]**ipsum**[/b] [i]dolor[/i] [u]met[/u].

Lorem [b]**ipsum[/b]** [i]dolor[/i] [u]met[/u].

Lorem [b]__ipsum[/b]__ [i]dolor[/i] [u]met[/u].

Lorem [b][i]ipsum[/i][/b].

Lorem [b][i]ipsum[/b][/i].

Lorem [b]ipsum[/B].
""".strip()

        expected_result = """
<p>Lorem <strong>ipsum</strong>, dolor met.</p>
<p>Lorem <b>ipsum</b>, <i>dolor</i> <u>met</u>.</p>
<p>Lorem <b><strong>ipsum</strong></b> <i>dolor</i> <u>met</u>.</p>
<p>Lorem <b>**ipsum</b>** <i>dolor</i> <u>met</u>.</p>
<p>Lorem <b>__ipsum</b>__ <i>dolor</i> <u>met</u>.</p>
<p>Lorem <b><i>ipsum</i></b>.</p>
<p>Lorem <b>[i]ipsum</b>[/i].</p>
<p>Lorem <b>ipsum</b>.</p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_hr(self):
        """hr bbcode is correctly parsed"""
        test_text = """
Lorem ipsum.
[hr]
Dolor met.
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<hr/>
<p>Dolor met.</p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_img(self):
        """img bbcode is correctly parsed"""
        test_text = """
Lorem ipsum [img]https://placekitten.com/g/1200/500[/img]

Lorem ipsum [iMg]https://placekitten.com/g/1200/500[/ImG]

Lorem ipsum !(https://placekitten.com/g/1200/500)
""".strip()

        expected_result = """
<p>Lorem ipsum <img alt="placekitten.com/g/1200/500" src="https://placekitten.com/g/1200/500"/></p>
<p>Lorem ipsum <img alt="placekitten.com/g/1200/500" src="https://placekitten.com/g/1200/500"/></p>
<p>Lorem ipsum <img alt="placekitten.com/g/1200/500" src="https://placekitten.com/g/1200/500"/></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_url(self):
        """url bbcode is correctly parsed"""
        test_text = """
Lorem ipsum [url]placekitten.com/g/300/300[/url]

Lorem ipsum [url]https://placekitten.com/g/600/600[/url]

Lorem ipsum [uRL=https://placekitten.com/g/400/400"]Label text![/UrL]

Lorem ipsum [Lorem ipsum](https://placekitten.com/g/1200/500)
""".strip()

        expected_result = """
<p>Lorem ipsum <a href="http://placekitten.com/g/300/300" rel="nofollow">placekitten.com/g/300/300</a></p>
<p>Lorem ipsum <a href="https://placekitten.com/g/600/600" rel="nofollow">placekitten.com/g/600/600</a></p>
<p>Lorem ipsum <a href="https://placekitten.com/g/400/400" rel="nofollow">Label text!</a></p>
<p>Lorem ipsum <a href="https://placekitten.com/g/1200/500" rel="nofollow">Lorem ipsum</a></p>
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

    def test_complex_paragraph(self):
        """parser minifies complex paragraph"""
        user = UserModel.objects.create_user('Bob', 'bob@test.com', 'Pass123')

        test_text = """
Hey there @{}, how's going?
""".strip().format(user)

        expected_result = """
<p>Hey there <a href="{}">@{}</a>, how's going?</p>
""".strip().format(user.get_absolute_url(), user)

        result = parse(test_text, MockRequest(user), user, minify=True)
        self.assertEqual(expected_result, result['parsed_text'])


class CleanLinksTests(TestCase):
    def test_clean_current_link(self):
        """clean_links step cleans http://test.com"""
        test_text = """
Lorem ipsum: http://test.com
""".strip()

        expected_result = """
<p>Lorem ipsum: <a href="/" rel="nofollow">test.com</a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])
        self.assertEqual(result['internal_links'], ['/'])
        self.assertEqual(result['images'], [])
        self.assertEqual(result['outgoing_links'], [])

    def test_clean_schemaless_link(self):
        """clean_links step cleans test.com"""
        test_text = """
Lorem ipsum: test.com
""".strip()

        expected_result = """
<p>Lorem ipsum: <a href="/" rel="nofollow">test.com</a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])
        self.assertEqual(result['internal_links'], ['/'])
        self.assertEqual(result['images'], [])
        self.assertEqual(result['outgoing_links'], [])

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
        self.assertEqual(result['internal_links'], ['/somewhere-something/'])
        self.assertEqual(result['images'], [])
        self.assertEqual(result['outgoing_links'], [])

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
        self.assertEqual(result['outgoing_links'], ['somewhere.com'])
        self.assertEqual(result['images'], [])
        self.assertEqual(result['internal_links'], [])

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
        self.assertEqual(result['outgoing_links'], ['somewhere.com/somewhere-something/'])
        self.assertEqual(result['images'], [])
        self.assertEqual(result['internal_links'], [])

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
        self.assertEqual(result['images'], ['/image.jpg'])
        self.assertEqual(result['internal_links'], [])
        self.assertEqual(result['outgoing_links'], [])

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
        self.assertEqual(result['images'], ['somewhere.com/image.jpg'])
        self.assertEqual(result['internal_links'], [])
        self.assertEqual(result['outgoing_links'], [])

    def test_clean_linked_image(self):
        """parser handles image element nested in link"""
        test_text = """
[![3.png](http://test.com/a/thumb/test/43/)](http://test.com/a/test/43/)
        """.strip()

        expected_result = """
<p><a href="/a/test/43/"><img alt="3.png" src="/a/thumb/test/43/"/></a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])
        self.assertEqual(result['images'], ['/a/thumb/test/43/'])
        self.assertEqual(result['internal_links'], ['/a/test/43/'])
        self.assertEqual(result['outgoing_links'], [])

    def test_force_shva(self):
        """parser appends ?shva=1 bit to attachment links if flag is present"""
        test_text = """
![3.png](http://test.com/a/thumb/test/43/)
        """.strip()

        expected_result = """
<p><img alt="3.png" src="/a/thumb/test/43/?shva=1"/></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True, force_shva=True)
        self.assertEqual(expected_result, result['parsed_text'])
        self.assertEqual(result['images'], ['/a/thumb/test/43/'])
        self.assertEqual(result['internal_links'], [])
        self.assertEqual(result['outgoing_links'], [])

    def test_remove_shva(self):
        """parser removes ?shva=1 bit from attachment links if flag is absent"""
        test_text = """
![3.png](http://test.com/a/thumb/test/43/?shva=1)
        """.strip()

        expected_result = """
<p><img alt="3.png" src="/a/thumb/test/43/"/></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])
        self.assertEqual(result['images'], ['/a/thumb/test/43/?shva=1'])
        self.assertEqual(result['internal_links'], [])
        self.assertEqual(result['outgoing_links'], [])


class LinkifyTests(TestCase):
    def test_clean_current_link(self):
        """clean_links step cleans http://test.com"""
        test_text = """
Lorem ipsum: `<http://test.com>`
""".strip()

        expected_result = """
<p>Lorem ipsum: <code>&lt;http://test.com&gt;</code></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result['parsed_text'])
        self.assertEqual(result['internal_links'], [])
        self.assertEqual(result['images'], [])
        self.assertEqual(result['outgoing_links'], [])


class StriketroughTests(TestCase):
    def test_striketrough(self):
        """striketrough markdown deletes test"""
        test_text = """
Lorem ~~ipsum, dolor~~ met.
""".strip()

        expected_result = """
<p>Lorem <del>ipsum, dolor</del> met.</p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])


class QuoteTests(TestCase):
    def test_quotes(self):
        """bbcode for quote is supported"""
        test_text = """
Lorem ipsum.
[quote]Dolor met[/quote]
[quote]Dolor <b>met</b>[/quote]
[quote]Dolor **met**[quote]Dolor met[/quote][/quote]
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Dolor met</p>
</blockquote>
</aside>
<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Dolor &lt;b&gt;met&lt;/b&gt;</p>
</blockquote>
</aside>
<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Dolor <strong>met</strong></p>
<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Dolor met</p>
</blockquote>
</aside>
</blockquote>
</aside>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_authored_quotes(self):
        """bbcode for authored quote is supported and handles mentions as well"""
        test_text = """
Lorem ipsum.
[quote]Dolor met[/quote]
[quote=\"@Bob\"]Dolor <b>met</b>[/quote]
[quote]Dolor **met**[quote=@Bob]Dolor met[/quote][/quote]
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Dolor met</p>
</blockquote>
</aside>
<aside class="quote-block">
<div class="quote-heading">@Bob</div>
<blockquote class="quote-body">
<p>Dolor &lt;b&gt;met&lt;/b&gt;</p>
</blockquote>
</aside>
<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Dolor <strong>met</strong></p>
<aside class="quote-block">
<div class="quote-heading">@Bob</div>
<blockquote class="quote-body">
<p>Dolor met</p>
</blockquote>
</aside>
</blockquote>
</aside>
""".strip()

        request = MockRequest(user=MockPoster())
        result = parse(test_text, request, MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_custom_quote_title(self):
        """parser handles custom quotetitle"""
        test_text = """
Lorem ipsum.
[quote=\"Lorem ipsum very test\"]Dolor <b>met</b>[/quote]
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<aside class="quote-block">
<div class="quote-heading">Lorem ipsum very test</div>
<blockquote class="quote-body">
<p>Dolor &lt;b&gt;met&lt;/b&gt;</p>
</blockquote>
</aside>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_hr_edge_case(self):
        """test for weird edge case in which hr gets moved outside of quote"""
        test_text = """
Lorem ipsum.
[quote]
Dolor met
- - - - -
Amet elit
[/quote]
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Dolor met</p>
<hr/>
<p>Amet elit</p>
</blockquote>
</aside>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])


class CodeTests(TestCase):
    def test_code(self):
        """code bbcode is correctly parsed"""
        test_text = """
Lorem ipsum.
[code]
Dolor [b]met.[/b]
[/code]
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<pre><code>Dolor [b]met.[/b]</code></pre>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_inline_code(self):
        """inline code bbcode is correctly parsed"""
        test_text = """
Lorem ipsum.

[code]Dolor [b]met.[/b][/code]
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<pre><code>Dolor [b]met.[/b]</code></pre>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_code_strip(self):
        """code bbcode trims its content"""
        test_text = """
Lorem ipsum.

[code]

   Dolor [b]met.[/b]


[/code]
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<pre><code>   Dolor [b]met.[/b]</code></pre>
""".strip()
        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_code_language(self):
        """code bbcode with language is correctly parsed"""
        test_text = """
Lorem ipsum.

[code="python"]
Dolor [b]met.[/b]
[/code]
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<pre><code class="python">Dolor [b]met.[/b]</code></pre>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_code_language_optional_quotes(self):
        """code quotes around language name are optional"""
        test_text = """
Lorem ipsum.

[code=python"]
Dolor [b]met.[/b]
[/code]
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<pre><code class="python">Dolor [b]met.[/b]</code></pre>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])

        test_text = """
Lorem ipsum.

[code="python]
Dolor [b]met.[/b]
[/code]
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<pre><code class="python">Dolor [b]met.[/b]</code></pre>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=False)
        self.assertEqual(expected_result, result['parsed_text'])
