# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_absolute_link_to_site_is_changed_to_relative_link 1"
] = '<p>clean_links step cleans <a href="/" target="_blank">example.com</a></p>'

snapshots[
    "test_absolute_link_to_site_without_schema_is_changed_to_relative_link 1"
] = '<p>clean_links step cleans <a href="/" target="_blank">example.com</a></p>'

snapshots[
    "test_absolute_link_with_path_to_site_is_changed_to_relative_link 1"
] = '<p>clean_links step cleans <a href="/somewhere-something/" target="_blank">example.com/somewhere-something/</a></p>'

snapshots[
    "test_local_image_is_changed_to_relative_link 1"
] = '<p>clean_links step cleans <img alt="example.com/media/img.png" src="/media/img.png" /></p>'

snapshots[
    "test_parser_converts_unmarked_links_to_hrefs 1"
] = '<p>Lorem ipsum <a href="http://test.com" rel="external nofollow noopener" target="_blank">test.com</a></p>'

snapshots[
    "test_parser_skips_links_in_code_bbcode 1"
] = "<pre><code>http://test.com</code></pre>"

snapshots[
    "test_parser_skips_links_in_inline_code_bbcode 1"
] = """<p>Lorem ipsum <br />
</p><pre><code>http://test.com</code></pre><p></p>"""

snapshots[
    "test_parser_skips_links_in_inline_code_markdown 1"
] = "<p>Lorem ipsum <code>http://test.com</code></p>"
