from django.test import TestCase

from ..parser import parse


def test_html_is_escaped(request_mock, user, snapshot):
    text = "Lorem <strong>ipsum!</strong>"
    result = parse(text, request_mock, user, minify=True)
    snapshot.assert_match(result["parsed_text"])


def test_parsed_text_is_minified(request_mock, user, snapshot):
    text = """
Lorem **ipsum** dolor met.

Sit amet elit.
"""
    result = parse(text, request_mock, user, minify=True)
    snapshot.assert_match(result["parsed_text"])


def test_parser_converts_unmarked_links_to_hrefs(request_mock, user, snapshot):
    text = "Lorem ipsum http://test.com"
    result = parse(text, request_mock, user, minify=True)
    snapshot.assert_match(result["parsed_text"])


def test_parser_skips_links_in_inline_code_markdown(request_mock, user, snapshot):
    text = "Lorem ipsum `http://test.com`"
    result = parse(text, request_mock, user, minify=True)
    snapshot.assert_match(result["parsed_text"])


def test_parser_skips_links_in_inline_code_bbcode(request_mock, user, snapshot):
    text = "Lorem ipsum [code]http://test.com[/code]"
    result = parse(text, request_mock, user, minify=True)
    snapshot.assert_match(result["parsed_text"])


class MockRequest:
    scheme = "http"

    def __init__(self, user=None):
        self.user = user

    def get_host(self):
        return "test.com"


class MockPoster:
    username = "LoremIpsum"
    slug = "loremipsum"


class CleanLinksTests(TestCase):
    def test_clean_current_link(self):
        """clean_links step cleans http://test.com"""
        test_text = """
Lorem ipsum: http://test.com
""".strip()

        expected_result = """
<p>Lorem ipsum: <a href="/">test.com</a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result["parsed_text"])
        self.assertEqual(result["internal_links"], ["/"])
        self.assertEqual(result["images"], [])
        self.assertEqual(result["outgoing_links"], [])

    def test_clean_schemaless_link(self):
        """clean_links step cleans test.com"""
        test_text = """
Lorem ipsum: test.com
""".strip()

        expected_result = """
<p>Lorem ipsum: <a href="/">test.com</a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result["parsed_text"])
        self.assertEqual(result["internal_links"], ["/"])
        self.assertEqual(result["images"], [])
        self.assertEqual(result["outgoing_links"], [])

    def test_trim_current_path(self):
        """clean_links step leaves http://test.com path"""
        test_text = """
Lorem ipsum: http://test.com/somewhere-something/
""".strip()

        expected_result = """
<p>Lorem ipsum: <a href="/somewhere-something/">test.com/somewhere-something/</a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result["parsed_text"])
        self.assertEqual(result["internal_links"], ["/somewhere-something/"])
        self.assertEqual(result["images"], [])
        self.assertEqual(result["outgoing_links"], [])

    def test_clean_outgoing_link_domain(self):
        """clean_links step leaves outgoing domain link"""
        test_text = """
Lorem ipsum: http://somewhere.com
""".strip()

        expected_result = """
<p>Lorem ipsum: <a href="http://somewhere.com" rel="nofollow noopener">somewhere.com</a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result["parsed_text"])
        self.assertEqual(result["outgoing_links"], ["somewhere.com"])
        self.assertEqual(result["images"], [])
        self.assertEqual(result["internal_links"], [])

    def test_trim_outgoing_path(self):
        """clean_links step leaves outgoing link domain and path"""
        test_text = """
Lorem ipsum: http://somewhere.com/somewhere-something/
""".strip()

        expected_result = """
<p>Lorem ipsum: <a href="http://somewhere.com/somewhere-something/" rel="nofollow noopener">somewhere.com/somewhere-something/</a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result["parsed_text"])
        self.assertEqual(
            result["outgoing_links"], ["somewhere.com/somewhere-something/"]
        )
        self.assertEqual(result["images"], [])
        self.assertEqual(result["internal_links"], [])

    def test_clean_local_image_src(self):
        """clean_links step cleans local image src"""
        test_text = """
!(http://test.com/image.jpg)
""".strip()

        expected_result = """
<p><img alt="test.com/image.jpg" src="/image.jpg"/></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result["parsed_text"])
        self.assertEqual(result["images"], ["/image.jpg"])
        self.assertEqual(result["internal_links"], [])
        self.assertEqual(result["outgoing_links"], [])

    def test_clean_remote_image_src(self):
        """clean_links step cleans remote image src"""
        test_text = """
!(http://somewhere.com/image.jpg)
""".strip()

        expected_result = """
<p><img alt="somewhere.com/image.jpg" src="http://somewhere.com/image.jpg"/></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result["parsed_text"])
        self.assertEqual(result["images"], ["somewhere.com/image.jpg"])
        self.assertEqual(result["internal_links"], [])
        self.assertEqual(result["outgoing_links"], [])

    def test_clean_linked_image(self):
        """parser handles image element nested in link"""
        test_text = """
[![3.png](http://test.com/a/thumb/test/43/)](http://test.com/a/test/43/)
        """.strip()

        expected_result = """
<p><a href="/a/test/43/"><img alt="3.png" src="/a/thumb/test/43/"/></a></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result["parsed_text"])
        self.assertEqual(result["images"], ["/a/thumb/test/43/"])
        self.assertEqual(result["internal_links"], ["/a/test/43/"])
        self.assertEqual(result["outgoing_links"], [])

    def test_force_shva(self):
        """parser appends ?shva=1 bit to attachment links if flag is present"""
        test_text = """
![3.png](http://test.com/a/thumb/test/43/)
        """.strip()

        expected_result = """
<p><img alt="3.png" src="/a/thumb/test/43/?shva=1"/></p>
""".strip()

        result = parse(
            test_text, MockRequest(), MockPoster(), minify=True, force_shva=True
        )
        self.assertEqual(expected_result, result["parsed_text"])
        self.assertEqual(result["images"], ["/a/thumb/test/43/"])
        self.assertEqual(result["internal_links"], [])
        self.assertEqual(result["outgoing_links"], [])

    def test_remove_shva(self):
        """parser removes ?shva=1 bit from attachment links if flag is absent"""
        test_text = """
![3.png](http://test.com/a/thumb/test/43/?shva=1)
        """.strip()

        expected_result = """
<p><img alt="3.png" src="/a/thumb/test/43/"/></p>
""".strip()

        result = parse(test_text, MockRequest(), MockPoster(), minify=True)
        self.assertEqual(expected_result, result["parsed_text"])
        self.assertEqual(result["images"], ["/a/thumb/test/43/?shva=1"])
        self.assertEqual(result["internal_links"], [])
        self.assertEqual(result["outgoing_links"], [])
