# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_html_is_escaped 1"] = "<p>Lorem &lt;strong&gt;ipsum!&lt;/strong&gt;</p>"

snapshots[
    "test_parsed_text_is_minified 1"
] = "<p>Lorem <strong>ipsum</strong> dolor met.</p><p>Sit amet elit.</p>"

snapshots[
    "test_parser_converts_unmarked_links_to_hrefs 1"
] = '<p>Lorem ipsum <a href="http://test.com" rel="nofollow noopener">test.com</a></p>'

snapshots[
    "test_parser_skips_links_in_inline_code_markdown 1"
] = "<p>Lorem ipsum <code>http://test.com</code></p>"

snapshots[
    "test_parser_skips_links_in_inline_code_bbcode 1"
] = "<p>Lorem ipsum <br/></p><pre><code>http://test.com</code></pre><p></p>"
